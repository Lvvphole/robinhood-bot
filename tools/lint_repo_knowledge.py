from __future__ import annotations

import re
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_AGENTS_LINES = 120
STALE_AFTER_DAYS = 90
CLAUDE_CANONICAL = "# CLAUDE.md\n\n@AGENTS.md\n"
PRODUCT_CONTRACT = "docs/product-specs/investment-decision-platform.md"
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

REQUIRED = [
    "AGENTS.md",
    "CLAUDE.md",
    "ARCHITECTURE.md",
    "docs/DESIGN.md",
    "docs/PLANS.md",
    "docs/PRODUCT_SENSE.md",
    "docs/QUALITY_SCORE.md",
    "docs/RELIABILITY.md",
    "docs/SECURITY.md",
    "docs/design-docs/index.md",
    "docs/design-docs/core-beliefs.md",
    "docs/design-docs/multifactor-graph.md",
    "docs/exec-plans/active/agent-first-graph-migration.md",
    "docs/exec-plans/completed/index.md",
    "docs/exec-plans/tech-debt-tracker.md",
    "docs/generated/repo-map.md",
    "docs/product-specs/index.md",
    PRODUCT_CONTRACT,
    "docs/product-specs/multifactor-research-system.md",
    "docs/references/evidence-index.md",
    "docs/references/harness-engineering.md",
]

GOVERNED_DIRS = [
    ROOT / "docs/design-docs",
    ROOT / "docs/exec-plans",
    ROOT / "docs/product-specs",
    ROOT / "docs/references",
]
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def governed_meta_docs() -> list[str]:
    paths = {"ARCHITECTURE.md"}
    for path in (ROOT / "docs").glob("*.md"):
        paths.add(path.relative_to(ROOT).as_posix())
    generated = ROOT / "docs/generated/repo-map.md"
    if generated.exists():
        paths.add(generated.relative_to(ROOT).as_posix())
    for directory in GOVERNED_DIRS:
        if directory.exists():
            for path in directory.rglob("*.md"):
                paths.add(path.relative_to(ROOT).as_posix())
    return sorted(paths)


def fail(message: str) -> None:
    print(f"ERROR: {message}")


def check_required(errors: list[str]) -> None:
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required repository-knowledge file: {rel}")


def check_agents_size(errors: list[str]) -> None:
    path = ROOT / "AGENTS.md"
    if not path.exists():
        return
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) > MAX_AGENTS_LINES:
        errors.append(
            f"AGENTS.md has {len(lines)} lines; max is {MAX_AGENTS_LINES}. "
            "Move detail into linked repository docs."
        )


def check_claude_contract(errors: list[str]) -> None:
    path = ROOT / "CLAUDE.md"
    if not path.exists():
        return
    if path.read_text(encoding="utf-8") != CLAUDE_CANONICAL:
        errors.append(
            "CLAUDE.md must exactly match the canonical compatibility entry point so @AGENTS.md "
            "cannot be hidden in a code fence or duplicated with divergent rules"
        )


def check_product_contract(errors: list[str]) -> None:
    path = ROOT / PRODUCT_CONTRACT
    if path.exists():
        text = path.read_text(encoding="utf-8")
        for heading in PRODUCT_CONTRACT_HEADINGS:
            if heading not in text:
                errors.append(f"canonical product contract missing {heading}")

    agents = ROOT / "AGENTS.md"
    if agents.exists():
        agents_text = agents.read_text(encoding="utf-8")
        if f"`{PRODUCT_CONTRACT}`" not in agents_text:
            errors.append(
                "AGENTS.md must point directly to the canonical product contract: "
                f"{PRODUCT_CONTRACT}"
            )


def check_metadata(errors: list[str]) -> None:
    for rel in governed_meta_docs():
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        for field in ("Status:", "Owner:", "Last verified:"):
            if field not in text:
                errors.append(f"{rel} missing metadata field {field}")


def check_freshness(errors: list[str]) -> None:
    today = date.today()
    for rel in governed_meta_docs():
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        status_match = re.search(r"^Status:\s*(.+)$", text, re.MULTILINE)
        verified_match = re.search(r"^Last verified:\s*(.+)$", text, re.MULTILINE)
        status = status_match.group(1).strip() if status_match else ""
        if status == "GENERATED":
            continue
        if not verified_match:
            continue
        raw = verified_match.group(1).strip()
        try:
            verified = datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            errors.append(f"{rel} has non-date Last verified value: {raw}")
            continue
        if verified > today:
            errors.append(f"{rel} has future Last verified date: {raw}")
            continue
        age = (today - verified).days
        if age > STALE_AFTER_DAYS:
            errors.append(
                f"{rel} is stale ({age} days since verification); review it and update Last verified."
            )


def check_links(errors: list[str]) -> None:
    for path in ROOT.rglob("*.md"):
        if any(part in {".git", ".pytest_cache"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        for target in LINK.findall(text):
            target = target.split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            candidate = (path.parent / target).resolve()
            try:
                candidate.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{path.relative_to(ROOT)} links outside repository: {target}")
                continue
            if not candidate.exists():
                errors.append(f"broken local link in {path.relative_to(ROOT)}: {target}")


def check_active_plan(errors: list[str]) -> None:
    path = ROOT / "docs/exec-plans/active/agent-first-graph-migration.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    for heading in (
        "## Goal",
        "## Non-goals",
        "## Baseline",
        "## Acceptance criteria",
        "## Progress",
        "## Decisions",
        "## Verification",
        "## Risks",
        "## Next action",
    ):
        if heading not in text:
            errors.append(f"active execution plan missing {heading}")


def main() -> int:
    errors: list[str] = []
    check_required(errors)
    check_agents_size(errors)
    check_claude_contract(errors)
    check_product_contract(errors)
    check_metadata(errors)
    check_freshness(errors)
    check_links(errors)
    check_active_plan(errors)
    if errors:
        for error in errors:
            fail(error)
        return 1
    print("repository knowledge contract: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
