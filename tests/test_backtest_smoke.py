from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

from zero_dte_bot.backtest import EventDrivenBacktester
from zero_dte_bot.config import BotConfig


def test_event_backtester_executes_one_deterministic_trade() -> None:
    root = Path(__file__).resolve().parents[1]
    cfg = BotConfig.load(root / "config" / "baseline.yaml").raw
    cfg["signal"]["minimum_volume_z"] = -10.0
    cfg["option_selection"]["minimum_open_interest"] = 1
    cfg["option_selection"]["minimum_contract_volume"] = 1

    start = datetime(2026, 7, 20, 13, 30, tzinfo=timezone.utc)  # 09:30 ET
    timestamps = [start + timedelta(minutes=5 * i) for i in range(14)]
    closes = [100.00, 100.05, 100.02, 100.08, 100.10, 100.12, 100.35, 100.50, 100.55, 100.60, 100.62, 100.63, 100.64, 100.65]
    bars = pd.DataFrame(
        {
            "timestamp": timestamps,
            "open": closes,
            "high": [x + 0.05 for x in closes],
            "low": [x - 0.05 for x in closes],
            "close": closes,
            "volume": [1000 + i * 100 for i in range(len(closes))],
            "vwap": [99.95 + i * 0.01 for i in range(len(closes))],
        }
    )
    option_rows = []
    premiums = [1.00, 1.02, 1.01, 1.03, 1.04, 1.05, 1.20, 1.80, 1.85, 1.90, 1.92, 1.93, 1.94, 1.95]
    for ts, premium in zip(timestamps, premiums, strict=True):
        option_rows.append(
            {
                "timestamp": ts,
                "expiration": "2026-07-20",
                "strike": 100.0,
                "right": "C",
                "bid": premium,
                "ask": premium + 0.04,
                "last": premium + 0.02,
                "volume": 1000,
                "open_interest": 5000,
                "implied_volatility": 0.25,
                "delta": 0.45,
                "gamma": 0.08,
                "theta": -0.12,
                "vega": 0.01,
                "symbol": "SPY260720C00100000",
            }
        )
    options = pd.DataFrame(option_rows)

    trades, metrics = EventDrivenBacktester(cfg).run(bars, options)
    assert len(trades) == 1
    assert trades[0].net_pnl > 0
    assert metrics["trades"] == 1
