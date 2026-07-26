from __future__ import annotations

import numpy as np


def bootstrap_daily_pnl(
    daily_pnl: np.ndarray,
    *,
    starting_equity: float,
    iterations: int = 10_000,
    seed: int = 23,
    ruin_fraction: float = 0.50,
) -> dict[str, float]:
    """Bootstrap daily P&L paths with deterministic sampling."""
    values = np.asarray(daily_pnl, dtype=float)
    if values.size == 0:
        return {
            "mean_daily_pnl_95_lower": 0.0,
            "mean_daily_pnl_95_upper": 0.0,
            "risk_of_ending_loss": 1.0,
            "risk_of_ruin": 1.0,
            "median_max_drawdown": 0.0,
        }
    rng = np.random.default_rng(seed)
    sampled = rng.choice(values, size=(iterations, values.size), replace=True)
    mean_daily = sampled.mean(axis=1)
    ending = starting_equity + sampled.sum(axis=1)
    paths = starting_equity + sampled.cumsum(axis=1)
    running_max = np.maximum.accumulate(paths, axis=1)
    drawdowns = paths - running_max
    max_drawdowns = drawdowns.min(axis=1)
    ruin_level = starting_equity * ruin_fraction
    ruined = (paths <= ruin_level).any(axis=1)
    return {
        "mean_daily_pnl_95_lower": float(np.quantile(mean_daily, 0.025)),
        "mean_daily_pnl_95_upper": float(np.quantile(mean_daily, 0.975)),
        "risk_of_ending_loss": float(np.mean(ending < starting_equity)),
        "risk_of_ruin": float(np.mean(ruined)),
        "median_max_drawdown": float(np.median(max_drawdowns)),
        "max_drawdown_95_worst": float(np.quantile(max_drawdowns, 0.05)),
    }
