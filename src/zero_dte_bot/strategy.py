from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import Iterable
from zoneinfo import ZoneInfo

import pandas as pd

from .models import OptionQuote, OptionRight

NY = ZoneInfo("America/New_York")


@dataclass(frozen=True, slots=True)
class Signal:
    timestamp: datetime
    direction: int
    reason: str


class OpeningRangeMomentumStrategy:
    """Single-hypothesis 0DTE strategy.

    The edge is sought in confirmed intraday directional continuation. The bot buys
    a liquid near-the-money option only after the underlying breaks the first
    30-minute range with VWAP, EMA, momentum, and volume confirmation.
    """

    def __init__(self, config: dict):
        self.market = config["market"]
        self.signal = config["signal"]
        self.selection = config["option_selection"]

    def opening_range(self, session: pd.DataFrame) -> tuple[float, float]:
        local = session["timestamp"].dt.tz_convert(NY)
        opening = session[(local.dt.time >= time(9, 30)) & (local.dt.time < time(10, 0))]
        if opening.empty:
            raise ValueError("Insufficient bars to calculate the opening range")
        return float(opening["high"].max()), float(opening["low"].min())

    def signal_for_bar(
        self,
        bar: pd.Series,
        *,
        opening_high: float,
        opening_low: float,
    ) -> Signal | None:
        ts = pd.Timestamp(bar["timestamp"]).to_pydatetime()
        local_time = ts.astimezone(NY).time()
        start = time.fromisoformat(self.market["entry_start"])
        end = time.fromisoformat(self.market["last_entry"])
        if not start <= local_time <= end:
            return None

        opening_fraction = (opening_high - opening_low) / float(bar["close"])
        if not (
            self.signal["minimum_opening_range_fraction"]
            <= opening_fraction
            <= self.signal["maximum_opening_range_fraction"]
        ):
            return None

        if pd.isna(bar["momentum"]) or pd.isna(bar["volume_z"]):
            return None

        threshold = float(self.signal["minimum_momentum_fraction"])
        volume_threshold = float(self.signal["minimum_volume_z"])
        bullish = (
            bar["close"] > opening_high
            and bar["close"] > bar["vwap"]
            and bar["ema_fast"] > bar["ema_slow"]
            and bar["momentum"] >= threshold
            and bar["volume_z"] >= volume_threshold
        )
        bearish = (
            bar["close"] < opening_low
            and bar["close"] < bar["vwap"]
            and bar["ema_fast"] < bar["ema_slow"]
            and bar["momentum"] <= -threshold
            and bar["volume_z"] >= volume_threshold
        )
        if bullish:
            return Signal(ts, 1, "opening_range_breakout_long")
        if bearish:
            return Signal(ts, -1, "opening_range_breakout_short")
        return None

    def select_option(
        self,
        *,
        signal: Signal,
        quotes: Iterable[OptionQuote],
    ) -> OptionQuote | None:
        target_right = OptionRight.CALL if signal.direction > 0 else OptionRight.PUT
        candidates: list[OptionQuote] = []
        for quote in quotes:
            if quote.right != target_right:
                continue
            if quote.expiration != signal.timestamp.astimezone(NY).date():
                continue
            quote_age = abs((signal.timestamp - quote.timestamp).total_seconds())
            if quote_age > self.selection["maximum_quote_age_seconds"]:
                continue
            abs_delta = abs(quote.delta)
            if not self.selection["minimum_abs_delta"] <= abs_delta <= self.selection["maximum_abs_delta"]:
                continue
            if quote.bid < self.selection["minimum_bid"]:
                continue
            if quote.open_interest < self.selection["minimum_open_interest"]:
                continue
            if quote.volume < self.selection["minimum_contract_volume"]:
                continue
            if quote.spread_fraction > self.selection["maximum_spread_fraction_of_mid"]:
                continue
            candidates.append(quote)

        if not candidates:
            return None
        target = float(self.selection["target_abs_delta"])
        return min(
            candidates,
            key=lambda q: (
                abs(abs(q.delta) - target),
                q.spread_fraction,
                -q.open_interest,
                -q.volume,
            ),
        )
