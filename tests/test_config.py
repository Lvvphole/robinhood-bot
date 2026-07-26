from pathlib import Path

from zero_dte_bot.config import BotConfig


def test_baseline_configuration_validates() -> None:
    root = Path(__file__).resolve().parents[1]
    cfg = BotConfig.load(root / "config" / "baseline.yaml")
    assert cfg.section("contract")["target_value"] == 200.0
    assert cfg.section("execution")["allow_live_trading"] is False
