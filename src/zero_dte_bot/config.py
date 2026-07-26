from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


class ConfigurationError(ValueError):
    """Raised when the strategy configuration violates an invariant."""


@dataclass(frozen=True, slots=True)
class BotConfig:
    raw: dict[str, Any]

    @classmethod
    def load(cls, path: str | Path) -> "BotConfig":
        with Path(path).open("r", encoding="utf-8") as handle:
            raw = yaml.safe_load(handle)
        config = cls(raw=raw)
        config.validate()
        return config

    def section(self, name: str) -> dict[str, Any]:
        value = self.raw.get(name)
        if not isinstance(value, dict):
            raise ConfigurationError(f"Missing configuration section: {name}")
        return value

    def validate(self) -> None:
        contract = self.section("contract")
        risk = self.section("risk")
        execution = self.section("execution")

        baseline = float(contract["baseline_value"])
        target = float(contract["target_value"])
        gap = float(contract["gap_value"])
        current = float(contract["current_value"])
        delta = float(contract["progress_delta_value"])
        tolerance = 1e-9

        if contract["target_direction"] != "increase":
            raise ConfigurationError("This contract must use target_direction=increase.")
        if abs(gap - (target - baseline)) > tolerance:
            raise ConfigurationError("gap_value violates the relational validation rule.")
        if abs(delta - (current - baseline)) > tolerance:
            raise ConfigurationError("progress_delta_value violates the relational validation rule.")
        if float(risk["starting_equity"]) <= 0:
            raise ConfigurationError("starting_equity must be positive.")
        if not 0 < float(risk["max_capital_at_risk_fraction"]) <= 0.05:
            raise ConfigurationError("max_capital_at_risk_fraction must be in (0, 0.05].")
        if bool(execution["allow_live_trading"]):
            raise ConfigurationError("Version 0.1 is research/paper-only; live trading must remain disabled.")
