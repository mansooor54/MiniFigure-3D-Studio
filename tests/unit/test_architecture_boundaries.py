from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Final

_ROOT: Final[Path] = Path(__file__).resolve().parents[2]
_DOMAIN_ROOTS: Final[tuple[Path, ...]] = (_ROOT / "app" / "models", _ROOT / "app" / "ports")
_FORBIDDEN_PREFIXES: Final[tuple[str, ...]] = (
    "PySide6",
    "bpy",
    "requests",
    "httpx",
    "subprocess",
    "app.adapters",
    "app.controllers",
    "app.services",
    "app.ui",
)


@dataclass(frozen=True)
class ForbiddenImport:
    filename: str
    line: int
    module: str


def find_forbidden_imports(source: str, filename: str) -> tuple[ForbiddenImport, ...]:
    tree = ast.parse(source, filename=filename)
    findings: list[ForbiddenImport] = []
    for node in ast.walk(tree):
        modules: tuple[str, ...] = ()
        if isinstance(node, ast.Import):
            modules = tuple(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            modules = (node.module,)
        for module in modules:
            if module.startswith(_FORBIDDEN_PREFIXES):
                findings.append(
                    ForbiddenImport(
                        filename=filename,
                        line=getattr(node, "lineno", 0),
                        module=module,
                    )
                )
    return tuple(findings)


def test_domain_and_ports_have_no_forbidden_imports() -> None:
    findings: list[ForbiddenImport] = []
    for root in _DOMAIN_ROOTS:
        for source_path in sorted(root.rglob("*.py")):
            findings.extend(
                find_forbidden_imports(
                    source_path.read_text(encoding="utf-8"),
                    source_path.relative_to(_ROOT).as_posix(),
                )
            )
    assert findings == []


def test_seeded_forbidden_import_is_detected() -> None:
    source = "from PySide6.QtCore import QObject\n"
    findings = find_forbidden_imports(source, "seeded_domain_module.py")
    assert findings == (
        ForbiddenImport(
            filename="seeded_domain_module.py",
            line=1,
            module="PySide6.QtCore",
        ),
    )
