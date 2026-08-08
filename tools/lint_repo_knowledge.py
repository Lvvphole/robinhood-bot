from __future__ import annotations

import re
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_AGENTS_LINES = 120
STALE_AFTER_DAYS = 90

REQUIRED = [
    "AGENTS.md",
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
