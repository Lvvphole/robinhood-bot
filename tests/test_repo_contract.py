from __future__ import annotations

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
