from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from lint_architecture import LAYER_ORDER, lint_tree


def make_package(tmp_path: Path) -> Path:
    package = tmp_path / "src" / "investment_platform"
    for rel in ("", *LAYER_ORDER):
        directory = package / rel if rel else package
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "__init__.py").write_text("", encoding="utf-8")
    return package


def messages(package: Path) -> list[str]:
    return [violation.message for violation in lint_tree(package)]


def test_current_target_package_boundaries_pass() -> None:
    assert lint_tree(ROOT / "src" / "investment_platform") == []


def test_runtime_may_compose_services_and_providers(tmp_path: Path) -> None:
    package = make_package(tmp_path)
    (package / "runtime" / "wire.py").write_text(
        "from investment_platform.services import portfolio\n"
        "from investment_platform.providers import broker\n",
        encoding="utf-8",
    )
    assert lint_tree(package) == []


def test_service_cannot_import_runtime_or_provider_implementation(tmp_path: Path) -> None:
    package = make_package(tmp_path)
    (package / "services" / "portfolio.py").write_text(
        "from investment_platform.runtime import scheduler\n"
        "from ..providers import market_data\n",
        encoding="utf-8",
    )
    result = messages(package)
    assert any("layer 'services' may not import layer 'runtime'" in message for message in result)
    assert any("layer 'services' may not import layer 'providers'" in message for message in result)


def test_unknown_top_level_layer_fails_closed(tmp_path: Path) -> None:
    package = make_package(tmp_path)
    experimental = package / "experimental"
    experimental.mkdir()
    (experimental / "__init__.py").write_text("", encoding="utf-8")
    result = messages(package)
    assert any("unknown target architecture layer 'experimental'" in message for message in result)


def test_root_reexport_cannot_bypass_layer_policy(tmp_path: Path) -> None:
    package = make_package(tmp_path)
    (package / "__init__.py").write_text(
        "from investment_platform.runtime import scheduler\n",
        encoding="utf-8",
    )
    (package / "services" / "portfolio.py").write_text(
        "from investment_platform import runtime\n",
        encoding="utf-8",
    )
    result = messages(package)
    assert any("root package must not import governed layer 'runtime'" in message for message in result)
    assert any("ambiguous root import 'investment_platform' is prohibited" in message for message in result)


def test_missing_layer_package_marker_fails_closed(tmp_path: Path) -> None:
    package = make_package(tmp_path)
    (package / "providers" / "__init__.py").unlink()
    result = messages(package)
    assert any("required package marker is missing" in message for message in result)
