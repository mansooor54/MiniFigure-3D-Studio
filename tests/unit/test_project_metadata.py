from __future__ import annotations

import re
import tomllib
from pathlib import Path
from typing import Final

_ROOT: Final[Path] = Path(__file__).resolve().parents[2]
_SEPARATOR: Final[re.Pattern[str]] = re.compile(r"[-_.]+")


def _normalize_requirement(requirement: str) -> str:
    name = requirement.split("[", maxsplit=1)[0]
    for separator in ("<", ">", "=", "!", "~", ";"):
        name = name.split(separator, maxsplit=1)[0]
    return _SEPARATOR.sub("-", name).strip().lower()


def _requirement_names(path: Path) -> set[str]:
    names: set[str] = set()
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith(("#", "-r ")):
            continue
        names.add(_normalize_requirement(line))
    return names


def _project_metadata() -> dict[str, object]:
    with (_ROOT / "pyproject.toml").open("rb") as handle:
        return tomllib.load(handle)


def test_runtime_requirements_match_project_metadata() -> None:
    metadata = _project_metadata()
    project = metadata["project"]
    assert isinstance(project, dict)
    dependencies = project["dependencies"]
    assert isinstance(dependencies, list)
    expected = {_normalize_requirement(item) for item in dependencies}
    assert _requirement_names(_ROOT / "requirements.txt") == expected


def test_development_requirements_match_project_metadata() -> None:
    metadata = _project_metadata()
    project = metadata["project"]
    assert isinstance(project, dict)
    optional = project["optional-dependencies"]
    assert isinstance(optional, dict)
    dependencies = optional["dev"]
    assert isinstance(dependencies, list)
    expected = {_normalize_requirement(item) for item in dependencies}
    assert _requirement_names(_ROOT / "requirements-dev.txt") == expected


def test_python_version_pin_matches_supported_series() -> None:
    version = (_ROOT / ".python-version").read_text(encoding="utf-8").strip()
    assert version == "3.11.16"
    metadata = _project_metadata()
    project = metadata["project"]
    assert isinstance(project, dict)
    assert project["requires-python"] == ">=3.11,<3.12"
