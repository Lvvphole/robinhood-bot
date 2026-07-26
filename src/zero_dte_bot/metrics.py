from __future__ import annotations

from dataclasses import asdict

import numpy as np
import pandas as pd

from .models import Trade


def maximum_drawdown(equity: pd.Series) -> float:
    if equity.empty:
        return 0.0
    running_max = equity.cummax()
    return float((equity - running_max).min())


def summarize_trades(trades: list[Trade], starting_equity: float) -> dict[str, float]:
    if not trades:
        return {
            "trades": 0,
            "net_pnl": 0.0,
            "average_trade": 0.0,
            "win_rate": 0.0,
            "profit_factor": 0.0,
            "max_drawdown_dollars": 0.0,
            "max_drawdown_fraction": 0.0,
            "average_daily_pnl": 0.0,
            "median_daily_pnl": 0.0,
            "target_200_hit_rate": 0.0,
        }
    frame = pd.DataFrame(asdict(t) for t in trades)
    frame["session_date"] = pd.to_datetime(frame["exit_time"], utc=True).dt.date
    daily = frame.groupby("session_date")["net_pnl"].sum()
    equity = starting_equity + frame["net_pnl"].cumsum()
    gross_profit = frame.loc[frame["net_pnl"] > 0, "net_pnl"].sum()
    gross_loss = -frame.loc[frame["net_pnl"] < 0, "net_pnl"].sum()
    drawdown_dollars = maximum_drawdown(equity)
    return {
        "trades": int(len(frame)),
        "net_pnl": float(frame["net_pnl"].sum()),
        "average_trade": float(frame["net_pnl"].mean()),
        "win_rate": float((frame["net_pnl"] > 0).mean()),
        "profit_factor": float(gross_profit / gross_loss) if gross_loss > 0 else float("inf"),
        "max_drawdown_dollars": drawdown_dollars,
        "max_drawdown_fraction": abs(drawdown_dollars) / starting_equity,
        "average_daily_pnl": float(daily.mean()),
        "median_daily_pnl": float(daily.median()),
        "target_200_hit_rate": float((daily >= 200.0).mean()),
        "daily_pnl_std": float(daily.std(ddof=1)) if len(daily) > 1 else 0.0,
        "best_day": float(daily.max()),
        "worst_day": float(daily.min()),
    }
