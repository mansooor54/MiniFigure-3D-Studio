from __future__ import annotations

import argparse
import json
import re
import tomllib
from dataclasses import asdict, dataclass
from importlib import metadata
from pathlib import Path
from typing import Final

_NAME_SEPARATOR: Final[re.Pattern[str]] = re.compile(r"[-_.]+")
_LICENSE_FILE_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"(^|/)(licen[cs]e|copying|notice|authors)(\.|$)", re.IGNORECASE
)


@dataclass(frozen=True)
class LicenseRecord:
    name: str
    normalized_name: str
    version: str
    direct: bool
    license_expression: str
    license_classifiers: tuple[str, ...]
    project_urls: tuple[str, ...]
    copied_license_files: tuple[str, ...]


def _normalize_name(name: str) -> str:
    return _NAME_SEPARATOR.sub("-", name).lower()


def _dependency_name(requirement: str) -> str:
    name = requirement.split("[", maxsplit=1)[0]
    for separator in ("<", ">", "=", "!", "~", ";"):
        name = name.split(separator, maxsplit=1)[0]
    return _normalize_name(name.strip())


def _direct_dependencies(pyproject_path: Path) -> set[str]:
    with pyproject_path.open("rb") as handle:
        data = tomllib.load(handle)
    project = data["project"]
    requirements = list(project.get("dependencies", []))
    optional = project.get("optional-dependencies", {})
    if isinstance(optional, dict):
        for group in optional.values():
            requirements.extend(group)
    return {_dependency_name(requirement) for requirement in requirements}


def _metadata_values(dist: metadata.Distribution, key: str) -> tuple[str, ...]:
    return tuple(value for value in dist.metadata.get_all(key, []) if value.strip())


def _metadata_value(dist: metadata.Distribution, key: str) -> str | None:
    values = dist.metadata.get_all(key, [])
    return values[0] if values else None


def _license_expression(dist: metadata.Distribution) -> str:
    expression = _metadata_value(dist, "License-Expression")
    if expression is not None and expression.strip():
        return expression.strip()
    legacy = _metadata_value(dist, "License")
    if legacy is not None and legacy.strip() and legacy.strip().upper() != "UNKNOWN":
        return legacy.strip()
    classifiers = [
        value.removeprefix("License :: ")
        for value in _metadata_values(dist, "Classifier")
        if value.startswith("License :: ") and value != "License :: OSI Approved"
    ]
    if classifiers:
        return "CLASSIFIER: " + "; ".join(classifiers)
    return "UNKNOWN — REVIEW REQUIRED"


def _copy_license_files(
    dist: metadata.Distribution, output_root: Path, normalized_name: str
) -> tuple[str, ...]:
    copied: list[str] = []
    for package_file in dist.files or []:
        portable_path = str(package_file).replace("\\", "/")
        if _LICENSE_FILE_PATTERN.search(portable_path) is None:
            continue
        source = Path(str(dist.locate_file(package_file)))
        if not source.is_file() or source.stat().st_size > 2 * 1024 * 1024:
            continue
        destination = output_root / normalized_name / Path(portable_path).name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())
        copied.append(destination.relative_to(output_root.parent).as_posix())
    return tuple(sorted(set(copied)))


def collect(project_root: Path, output_root: Path) -> list[LicenseRecord]:
    direct_dependencies = _direct_dependencies(project_root / "pyproject.toml")
    records: list[LicenseRecord] = []
    installed_names: set[str] = set()
    for dist in sorted(metadata.distributions(), key=lambda item: _normalize_name(item.name)):
        normalized_name = _normalize_name(dist.name)
        installed_names.add(normalized_name)
        classifiers = tuple(
            value.removeprefix("License :: ")
            for value in _metadata_values(dist, "Classifier")
            if value.startswith("License :: ")
        )
        records.append(
            LicenseRecord(
                name=dist.name,
                normalized_name=normalized_name,
                version=dist.version,
                direct=normalized_name in direct_dependencies,
                license_expression=_license_expression(dist),
                license_classifiers=classifiers,
                project_urls=_metadata_values(dist, "Project-URL"),
                copied_license_files=_copy_license_files(dist, output_root, normalized_name),
            )
        )
    missing = sorted(direct_dependencies - installed_names)
    if missing:
        joined_names = ", ".join(missing)
        raise RuntimeError(
            f"Installed environment is missing direct dependencies: {joined_names}"
        )
    return records


def _write_json(records: list[LicenseRecord], output_path: Path) -> None:
    output_path.write_text(
        json.dumps([asdict(record) for record in records], indent=2, sort_keys=True),
        encoding="utf-8",
    )


def _write_markdown(records: list[LicenseRecord], output_path: Path) -> None:
    lines = [
        "# Development Dependency License Inventory",
        "",
        "This generated inventory is review evidence, not legal advice. "
        "`UNKNOWN` entries block release until resolved.",
        "",
        "| Package | Version | Direct | License Metadata | Copied Texts |",
        "|---|---:|:---:|---|---:|",
    ]
    for record in records:
        license_text = record.license_expression
        if record.license_classifiers:
            license_text += "; " + ", ".join(record.license_classifiers)
        lines.append(
            f"| {record.name} | {record.version} | {'Yes' if record.direct else 'No'} "
            f"| {license_text.replace('|', '/')} | {len(record.copied_license_files)} |"
        )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _parse_args() -> argparse.Namespace:
    project_root = Path(__file__).resolve().parents[1]
    default_report_root = project_root / "reports" / "generated"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=project_root)
    parser.add_argument("--report-root", type=Path, default=default_report_root)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    project_root = args.project_root.resolve()
    report_root = args.report_root.resolve()
    report_root.mkdir(parents=True, exist_ok=True)
    records = collect(project_root, report_root / "license-texts")
    _write_json(records, report_root / "development-licenses.json")
    _write_markdown(records, report_root / "development-licenses.md")
    direct_count = sum(record.direct for record in records)
    print(f"Collected {len(records)} packages; {direct_count} direct dependencies")


if __name__ == "__main__":
    main()
