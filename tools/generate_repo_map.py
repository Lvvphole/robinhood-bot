from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/generated/repo-map.md"
IGNORE_DIRS = {".git", ".pytest_cache", "__pycache__", ".mypy_cache", ".ruff_cache", ".venv", "venv"}


def paths() -> list[str]:
    result: list[str] = []
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT)
        if any(part in IGNORE_DIRS for part in rel.parts):
            continue
        if path == OUTPUT:
            continue
        if path.is_file():
            result.append(rel.as_posix())
    return sorted(result)


def render() -> str:
    body = "\n".join(f"- `{path}`" for path in paths())
    return (
        "# Generated Repository Map\n\n"
        "Status: GENERATED\n"
        "Owner: tools/generate_repo_map.py\n"
        "Last verified: generated at commit/worktree state\n\n"
        "Do not hand-edit. Regenerate with `python tools/generate_repo_map.py`.\n\n"
        f"{body}\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render()
    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if current != expected:
            print("ERROR: docs/generated/repo-map.md is stale; run python tools/generate_repo_map.py")
            return 1
        print("generated repository map: PASS")
        return 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(expected, encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
