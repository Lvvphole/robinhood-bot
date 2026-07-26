from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd

from .backtest import EventDrivenBacktester
from .config import BotConfig
from .monte_carlo import bootstrap_daily_pnl
from .validation import validate_research_result


def main() -> None:
    parser = argparse.ArgumentParser(description="0DTE strategy research runner")
    parser.add_argument("--config", default="config/baseline.yaml")
    parser.add_argument("--bars", required=True, help="Underlying 5-minute bars CSV/Parquet")
    parser.add_argument("--options", required=True, help="Option quote snapshots CSV/Parquet")
    parser.add_argument("--output", default="backtest_result.json")
    args = parser.parse_args()

    cfg = BotConfig.load(args.config).raw
    bars = _load_frame(args.bars)
    options = _load_frame(args.options)
    trades, metrics = EventDrivenBacktester(cfg).run(bars, options)

    if trades:
        trade_frame = pd.DataFrame(asdict(t) for t in trades)
        trade_frame["session_date"] = pd.to_datetime(trade_frame["exit_time"], utc=True).dt.date
        daily = trade_frame.groupby("session_date")["net_pnl"].sum().to_numpy(dtype=float)
    else:
        daily = np.array([], dtype=float)

    mc = bootstrap_daily_pnl(
        daily,
        starting_equity=float(cfg["risk"]["starting_equity"]),
        iterations=int(cfg["validation"]["monte_carlo_iterations"]),
        seed=int(cfg["validation"]["random_seed"]),
    )
    validation = validate_research_result(metrics, mc, cfg)
    result = {
        "metrics": metrics,
        "monte_carlo": mc,
        "validation": {"passed": validation.passed, "failures": validation.failures},
        "trade_count": len(trades),
    }
    Path(args.output).write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(json.dumps(result, indent=2, default=str))


def _load_frame(path: str) -> pd.DataFrame:
    source = Path(path)
    if source.suffix.lower() == ".parquet":
        return pd.read_parquet(source)
    return pd.read_csv(source)
