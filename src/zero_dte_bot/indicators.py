from __future__ import annotations

import numpy as np
import pandas as pd


def enrich_underlying_bars(
    bars: pd.DataFrame,
    *,
    fast_ema: int,
    slow_ema: int,
    momentum_lookback_bars: int,
    volume_z_lookback: int,
) -> pd.DataFrame:
    required = {"timestamp", "open", "high", "low", "close", "volume"}
    missing = required.difference(bars.columns)
    if missing:
        raise ValueError(f"Underlying data missing columns: {sorted(missing)}")

    frame = bars.sort_values("timestamp").copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame["session_date"] = frame["timestamp"].dt.tz_convert("America/New_York").dt.date
    frame["ema_fast"] = frame["close"].ewm(span=fast_ema, adjust=False).mean()
    frame["ema_slow"] = frame["close"].ewm(span=slow_ema, adjust=False).mean()
    frame["momentum"] = frame["close"].pct_change(momentum_lookback_bars)

    rolling_mean = frame["volume"].rolling(volume_z_lookback, min_periods=5).mean()
    rolling_std = frame["volume"].rolling(volume_z_lookback, min_periods=5).std(ddof=0)
    frame["volume_z"] = (frame["volume"] - rolling_mean) / rolling_std.replace(0, np.nan)

    if "vwap" not in frame.columns:
        typical = (frame["high"] + frame["low"] + frame["close"]) / 3.0
        pv = typical * frame["volume"]
        frame["vwap"] = pv.groupby(frame["session_date"]).cumsum() / frame["volume"].groupby(
            frame["session_date"]
        ).cumsum()
    return frame
