from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from lint_repo_knowledge import markdown_level_two_headings

CLAUDE_CANONICAL = "# CLAUDE.md\n\n@AGENTS.md\n"
PRODUCT_CONTRACT = ROOT / "docs/product-specs/investment-decision-platform.md"
PRODUCT_CONTRACT_HEADINGS = (
    "## Authority",
    "## User Story",
    "## User Experience",
    "## Goal",
    "## North Star",
    "## Desired State",
    "## Definition of Done",
    "## Non-goals",
    "## Success Measures",
    "## System Lifecycle",
)


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


def test_claude_code_contract_is_canonical_import() -> None:
    assert (ROOT / "CLAUDE.md").read_text(encoding="utf-8") == CLAUDE_CANONICAL


def test_canonical_product_contract_has_required_sections() -> None:
    headings = markdown_level_two_headings(PRODUCT_CONTRACT.read_text(encoding="utf-8"))
    for heading in PRODUCT_CONTRACT_HEADINGS:
        assert heading in headings


def test_product_heading_parser_rejects_noncanonical_contexts() -> None:
    text = """### Goal
## Goalkeeper
```markdown
## Goal
```
## User Story
"""
    headings = markdown_level_two_headings(text)
    assert "## Goal" not in headings
    assert "## User Story" in headings


def test_agents_points_to_canonical_product_contract() -> None:
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "`docs/product-specs/investment-decision-platform.md`" in text
