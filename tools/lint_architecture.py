from __future__ import annotations

import argparse
import ast
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "src"
PACKAGE_NAME = "investment_platform"
PACKAGE_ROOT = SOURCE_ROOT / PACKAGE_NAME

LAYER_ORDER = (
    "contracts",
    "config",
    "repositories",
    "services",
    "providers",
    "runtime",
    "interfaces",
)
LAYERS = frozenset(LAYER_ORDER)
ALLOWED_IMPORTS = {
    "contracts": frozenset({"contracts"}),
    "config": frozenset({"contracts", "config"}),
    "repositories": frozenset({"contracts", "config", "repositories"}),
    "services": frozenset({"contracts", "config", "repositories", "services"}),
    "providers": frozenset({"contracts", "config", "repositories", "providers"}),
    "runtime": frozenset(
        {"contracts", "config", "repositories", "services", "providers", "runtime"}
    ),
    "interfaces": frozenset(LAYERS),
}

# Known integration surfaces must remain behind provider adapters. This list is
# intentionally narrow: numerical/scientific libraries are not external-system
# boundaries, while broker/model/network SDKs and the quarantined legacy gateway are.
PROVIDER_ONLY_IMPORT_PREFIXES = (
    "zero_dte_bot.robinhood_gateway",
    "robin_stocks",
    "alpaca",
    "ib_insync",
    "openai",
    "anthropic",
    "httpx",
    "requests",
)


@dataclass(frozen=True, order=True)
class Violation:
    path: str
    line: int
    message: str

    def render(self) -> str:
        return f"{self.path}:{self.line}: {self.message}"


def source_layer(path: Path, package_root: Path = PACKAGE_ROOT) -> str | None:
    rel = path.relative_to(package_root)
    if rel == Path("__init__.py"):
        return None
    if not rel.parts:
        return None
    return rel.parts[0]


def _package_parts(path: Path, source_root: Path) -> list[str]:
    rel = path.relative_to(source_root)
    return list(rel.parent.parts)


def imported_modules(
    tree: ast.AST,
    *,
    path: Path,
    source_root: Path = SOURCE_ROOT,
) -> list[tuple[int, str]]:
    modules: list[tuple[int, str]] = []
    current_package = _package_parts(path, source_root)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.append((node.lineno, alias.name))
            continue
        if not isinstance(node, ast.ImportFrom):
            continue

        if node.level == 0:
            if node.module:
                modules.append((node.lineno, node.module))
            continue

        drop = node.level - 1
        if drop >= len(current_package):
            modules.append((node.lineno, PACKAGE_NAME))
            continue

        anchor = current_package[: len(current_package) - drop]
        if node.module:
            modules.append((node.lineno, ".".join(anchor + node.module.split("."))))
        else:
            for alias in node.names:
                modules.append((node.lineno, ".".join(anchor + [alias.name])))

    return modules


def target_layer(module: str, package_name: str = PACKAGE_NAME) -> str | None:
    parts = module.split(".")
    if not parts or parts[0] != package_name:
        return None
    if len(parts) == 1:
        return ""
    return parts[1]


def provider_only_import(module: str) -> str | None:
    for prefix in PROVIDER_ONLY_IMPORT_PREFIXES:
        if module == prefix or module.startswith(prefix + "."):
            return prefix
    return None


def lint_file(
    path: Path,
    *,
    package_root: Path = PACKAGE_ROOT,
    source_root: Path = SOURCE_ROOT,
    package_name: str = PACKAGE_NAME,
) -> list[Violation]:
    rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
    rel_text = rel.as_posix()
    layer = source_layer(path, package_root)

    if layer is None:
        if path.name != "__init__.py" or path.parent != package_root:
            return [Violation(rel_text, 1, "target package file is outside a governed layer")]
    elif layer not in LAYERS:
        return [
            Violation(
                rel_text,
                1,
                f"unknown target architecture layer '{layer}'; expected one of {', '.join(LAYER_ORDER)}",
            )
        ]

    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=rel_text)
    except (OSError, SyntaxError) as exc:
        line = getattr(exc, "lineno", None) or 1
        return [Violation(rel_text, line, f"cannot parse Python source: {exc}")]

    violations: list[Violation] = []
    for line, module in imported_modules(tree, path=path, source_root=source_root):
        provider_boundary = provider_only_import(module)
        if provider_boundary is not None and layer != "providers":
            violations.append(
                Violation(
                    rel_text,
                    line,
                    f"layer '{layer or 'root'}' may not import provider-only integration '{provider_boundary}' via '{module}'",
                )
            )
            continue

        imported = target_layer(module, package_name)
        if imported is None:
            continue
        if imported == "":
            violations.append(
                Violation(
                    rel_text,
                    line,
                    f"ambiguous root import '{package_name}' is prohibited; import a governed layer explicitly",
                )
            )
            continue
        if imported not in LAYERS:
            violations.append(
                Violation(
                    rel_text,
                    line,
                    f"import targets unknown architecture layer '{imported}' via '{module}'",
                )
            )
            continue
        if layer is None:
            violations.append(
                Violation(
                    rel_text,
                    line,
                    f"root package must not import governed layer '{imported}'",
                )
            )
            continue
        if imported not in ALLOWED_IMPORTS[layer]:
            violations.append(
                Violation(
                    rel_text,
                    line,
                    f"layer '{layer}' may not import layer '{imported}' via '{module}'",
                )
            )

    return violations


def lint_tree(package_root: Path = PACKAGE_ROOT) -> list[Violation]:
    if not package_root.is_dir():
        rel = package_root.relative_to(ROOT) if package_root.is_relative_to(ROOT) else package_root
        return [Violation(rel.as_posix(), 1, "target architecture package root is missing")]

    source_root = package_root.parent
    package_name = package_root.name
    violations: list[Violation] = []

    required_packages = [package_root, *(package_root / layer for layer in LAYER_ORDER)]
    for directory in required_packages:
        rel = directory.relative_to(ROOT) if directory.is_relative_to(ROOT) else directory
        if not directory.is_dir():
            violations.append(
                Violation(rel.as_posix(), 1, "required architecture layer package is missing")
            )
            continue
        init_file = directory / "__init__.py"
        if not init_file.is_file():
            init_rel = init_file.relative_to(ROOT) if init_file.is_relative_to(ROOT) else init_file
            violations.append(Violation(init_rel.as_posix(), 1, "required package marker is missing"))

    for path in sorted(package_root.rglob("*.py")):
        violations.extend(
            lint_file(
                path,
                package_root=package_root,
                source_root=source_root,
                package_name=package_name,
            )
        )
    return sorted(violations)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Enforce internal Python package dependency boundaries."
    )
    parser.parse_args()

    violations = lint_tree()
    if violations:
        for violation in violations:
            print(f"ERROR: {violation.render()}")
        return 1

    print("architecture dependency contract: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
