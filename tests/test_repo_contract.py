from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(script: str, *args: str) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / script), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_repository_knowledge_contract() -> None:
    run("tools/lint_repo_knowledge.py")


def test_generated_repo_map_is_current() -> None:
    run("tools/generate_repo_map.py", "--check")


def test_generated_repo_map_ignores_editable_install_metadata() -> None:
    metadata = ROOT / "src" / "contract_fixture.egg-info"
    metadata.mkdir()
    (metadata / "PKG-INFO").write_text("fixture\n", encoding="utf-8")
    try:
        run("tools/generate_repo_map.py", "--check")
    finally:
        shutil.rmtree(metadata)


def test_claude_code_contract_imports_agents() -> None:
    lines = (ROOT / "CLAUDE.md").read_text(encoding="utf-8").splitlines()
    assert "@AGENTS.md" in {line.strip() for line in lines}
