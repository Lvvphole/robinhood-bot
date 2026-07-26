from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValidationResult:
    passed: bool
    failures: tuple[str, ...]


def validate_research_result(
    metrics: dict[str, float],
    monte_carlo: dict[str, float],
    config: dict,
) -> ValidationResult:
    rules = config["validation"]
    failures: list[str] = []
    if metrics["trades"] < rules["minimum_out_of_sample_trades"]:
        failures.append("insufficient_out_of_sample_trades")
    if metrics["profit_factor"] < rules["minimum_profit_factor"]:
        failures.append("profit_factor_below_threshold")
    if metrics["max_drawdown_fraction"] > rules["maximum_drawdown_fraction"]:
        failures.append("maximum_drawdown_above_threshold")
    if (
        monte_carlo["mean_daily_pnl_95_lower"]
        <= rules["minimum_bootstrap_mean_daily_pnl_95_lower"]
    ):
        failures.append("bootstrap_lower_bound_not_positive")
    return ValidationResult(passed=not failures, failures=tuple(failures))


def validate_numeric_invariants(
    *,
    baseline: float,
    target: float,
    current: float,
    gap: float,
    progress_delta: float,
    tolerance: float = 1e-9,
) -> bool:
    expected_gap = target - baseline
    expected_delta = current - baseline
    return abs(gap - expected_gap) <= tolerance and abs(progress_delta - expected_delta) <= tolerance
