from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

import pandas as pd

from .execution import FillModel
from .indicators import enrich_underlying_bars
from .metrics import summarize_trades
from .models import OptionQuote, OptionRight, Position, Trade
from .strategy import OpeningRangeMomentumStrategy

NY = ZoneInfo("America/New_York")


class BacktestDataError(ValueError):
    """Raised when historical data cannot support a realistic backtest."""


def _quotes_from_frame(frame: pd.DataFrame) -> list[OptionQuote]:
    required = {
        "timestamp",
        "expiration",
        "strike",
        "right",
        "bid",
        "ask",
        "last",
        "volume",
        "open_interest",
        "implied_volatility",
        "delta",
        "gamma",
        "theta",
        "vega",
    }
    missing = required.difference(frame.columns)
    if missing:
        raise BacktestDataError(f"Option data missing columns: {sorted(missing)}")
    quotes: list[OptionQuote] = []
    for row in frame.itertuples(index=False):
        quotes.append(
            OptionQuote(
                timestamp=pd.Timestamp(row.timestamp).to_pydatetime(),
                expiration=pd.Timestamp(row.expiration).date(),
                strike=float(row.strike),
                right=OptionRight(str(row.right).upper()),
                bid=float(row.bid),
                ask=float(row.ask),
                last=float(row.last),
                volume=int(row.volume),
                open_interest=int(row.open_interest),
                implied_volatility=float(row.implied_volatility),
                delta=float(row.delta),
                gamma=float(row.gamma),
                theta=float(row.theta),
                vega=float(row.vega),
                symbol=str(getattr(row, "symbol", "")),
            )
        )
    return quotes


class EventDrivenBacktester:
    """Bar/quote event backtester with conservative fills and hard risk gates."""

    def __init__(self, config: dict):
        self.config = config
        self.strategy = OpeningRangeMomentumStrategy(config)
        self.fill_model = FillModel(config["execution"])
        self.multiplier = int(config["execution"]["contract_multiplier"])
        self.fee_each_way = float(config["execution"]["commission_per_contract_each_way"])

    def run(self, bars: pd.DataFrame, option_quotes: pd.DataFrame) -> tuple[list[Trade], dict[str, float]]:
        signal_cfg = self.config["signal"]
        enriched = enrich_underlying_bars(
            bars,
            fast_ema=int(signal_cfg["fast_ema"]),
            slow_ema=int(signal_cfg["slow_ema"]),
            momentum_lookback_bars=int(signal_cfg["momentum_lookback_bars"]),
            volume_z_lookback=int(signal_cfg["volume_z_lookback"]),
        )
        options = option_quotes.copy()
        options["timestamp"] = pd.to_datetime(options["timestamp"], utc=True)
        options["expiration"] = pd.to_datetime(options["expiration"]).dt.date
        options["session_date"] = options["timestamp"].dt.tz_convert(NY).dt.date

        trades: list[Trade] = []
        equity = float(self.config["risk"]["starting_equity"])
        risk_cfg = self.config["risk"]

        for session_date, session in enriched.groupby("session_date", sort=True):
            session = session.sort_values("timestamp")
            try:
                opening_high, opening_low = self.strategy.opening_range(session)
            except ValueError:
                continue
            session_options = options[options["session_date"] == session_date]
            position: Position | None = None
            trades_today = 0
            daily_pnl = 0.0
            consecutive_losses = 0

            for _, bar in session.iterrows():
                ts = pd.Timestamp(bar["timestamp"]).to_pydatetime()
                same_time = session_options[
                    (session_options["timestamp"] - pd.Timestamp(ts)).abs()
                    <= pd.Timedelta(seconds=self.config["option_selection"]["maximum_quote_age_seconds"])
                ]
                quotes = _quotes_from_frame(same_time)

                if position is not None:
                    current_quote = self._matching_quote(position, quotes)
                    if current_quote is not None:
                        mark = current_quote.bid
                        position.highest_mark = max(position.highest_mark, mark)
                        exit_reason = self._exit_reason(position, current_quote, bar)
                        if exit_reason:
                            trade = self._close(position, current_quote, ts, exit_reason)
                            trades.append(trade)
                            equity += trade.net_pnl
                            daily_pnl += trade.net_pnl
                            trades_today += 1
                            consecutive_losses = consecutive_losses + 1 if trade.net_pnl < 0 else 0
                            position = None
                    continue

                daily_loss_limit = equity * float(risk_cfg["daily_loss_limit_fraction"])
                if daily_pnl <= -daily_loss_limit:
                    continue
                if trades_today >= int(risk_cfg["max_trades_per_day"]):
                    continue
                if consecutive_losses >= int(risk_cfg["max_consecutive_losses"]):
                    continue

                signal = self.strategy.signal_for_bar(
                    bar, opening_high=opening_high, opening_low=opening_low
                )
                if signal is None:
                    continue
                selected = self.strategy.select_option(signal=signal, quotes=quotes)
                if selected is None:
                    continue
                entry_price = self.fill_model.buy_price(selected)
                full_premium_risk = entry_price * self.multiplier
                capital_budget = equity * float(risk_cfg["max_capital_at_risk_fraction"])
                quantity = min(
                    int(risk_cfg["max_contracts"]),
                    int(capital_budget // full_premium_risk) if full_premium_risk > 0 else 0,
                )
                if quantity < 1:
                    continue
                position = Position(
                    quote=selected,
                    quantity=quantity,
                    entry_time=ts,
                    entry_price=entry_price,
                    highest_mark=selected.bid,
                    direction=signal.direction,
                )

            if position is not None:
                last_ts = pd.Timestamp(session.iloc[-1]["timestamp"]).to_pydatetime()
                last_quotes = _quotes_from_frame(session_options.tail(50))
                current_quote = self._matching_quote(position, last_quotes)
                if current_quote is not None:
                    trade = self._close(position, current_quote, last_ts, "session_end")
                    trades.append(trade)
                    equity += trade.net_pnl

        metrics = summarize_trades(trades, float(risk_cfg["starting_equity"]))
        return trades, metrics

    @staticmethod
    def _matching_quote(position: Position, quotes: list[OptionQuote]) -> OptionQuote | None:
        matches = [
            q
            for q in quotes
            if q.right == position.quote.right
            and q.strike == position.quote.strike
            and q.expiration == position.quote.expiration
        ]
        return max(matches, key=lambda q: q.timestamp) if matches else None

    def _exit_reason(self, position: Position, quote: OptionQuote, bar: pd.Series) -> str | None:
        risk = self.config["risk"]
        now = quote.timestamp.astimezone(NY)
        hard_exit = time.fromisoformat(self.config["market"]["hard_exit"])
        if now.time() >= hard_exit:
            return "hard_exit"
        if quote.bid <= position.entry_price * (1.0 - float(risk["option_stop_loss_fraction"])):
            return "premium_stop"
        if quote.bid >= position.entry_price * (1.0 + float(risk["option_profit_target_fraction"])):
            return "profit_target"
        if now - position.entry_time.astimezone(NY) >= timedelta(minutes=int(risk["max_hold_minutes"])):
            return "time_stop"
        activation = position.entry_price * (1.0 + float(risk["trailing_activation_fraction"]))
        if position.highest_mark >= activation:
            floor = position.highest_mark * (1.0 - float(risk["trailing_giveback_fraction"]))
            if quote.bid <= floor:
                return "trailing_stop"
        if position.direction > 0 and bar["close"] < bar["vwap"]:
            return "underlying_vwap_invalidation"
        if position.direction < 0 and bar["close"] > bar["vwap"]:
            return "underlying_vwap_invalidation"
        return None

    def _close(self, position: Position, quote: OptionQuote, ts: datetime, reason: str) -> Trade:
        exit_price = self.fill_model.sell_price(quote)
        gross = (exit_price - position.entry_price) * self.multiplier * position.quantity
        fees = self.fee_each_way * 2.0 * position.quantity
        return Trade(
            symbol=position.quote.symbol,
            right=position.quote.right,
            strike=position.quote.strike,
            expiration=position.quote.expiration,
            quantity=position.quantity,
            entry_time=position.entry_time,
            exit_time=ts,
            entry_price=position.entry_price,
            exit_price=exit_price,
            gross_pnl=gross,
            fees=fees,
            net_pnl=gross - fees,
            exit_reason=reason,
            entry_delta=position.quote.delta,
            entry_gamma=position.quote.gamma,
            entry_theta=position.quote.theta,
            entry_vega=position.quote.vega,
        )
