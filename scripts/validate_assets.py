from __future__ import annotations

import argparse
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Final

import yaml

_SHA256_PATTERN: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{64}$")
_REQUIRED_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "path",
        "media_type",
        "source",
        "generator_version",
        "license",
        "sha256",
        "size_bytes",
        "contains_real_person",
        "contains_exif",
        "purpose",
        "expected",
    }
)
_IGNORED_NAMES: Final[frozenset[str]] = frozenset({".DS_Store", "asset_manifest.yaml"})


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    message: str

    def render(self) -> str:
        return f"{self.path}: {self.message}"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_relative_path(raw_path: object) -> Path | None:
    if not isinstance(raw_path, str) or not raw_path:
        return None
    candidate = Path(raw_path)
    if candidate.is_absolute() or ".." in candidate.parts:
        return None
    return candidate


def load_manifest(manifest_path: Path) -> dict[str, object]:
    content = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(content, dict):
        raise ValueError("Asset manifest root must be a mapping")
    return content


def _manifest_entries(data: dict[str, object]) -> list[dict[str, object]]:
    raw_assets = data.get("assets")
    if not isinstance(raw_assets, list):
        return []
    return [item for item in raw_assets if isinstance(item, dict)]


def _validate_policy(data: dict[str, object]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if data.get("schema_version") != 1:
        issues.append(ValidationIssue("asset_manifest.yaml", "schema_version must be 1"))
    policy = data.get("policy")
    if not isinstance(policy, dict):
        issues.append(ValidationIssue("asset_manifest.yaml", "policy must be a mapping"))
        return issues
    if policy.get("real_person_assets_allowed") is not False:
        issues.append(ValidationIssue("asset_manifest.yaml", "real-person assets must be disabled"))
    if policy.get("unmanifested_binary_assets_allowed") is not False:
        issues.append(
            ValidationIssue(
                "asset_manifest.yaml", "unmanifested binaries must be disabled"
            )
        )
    return issues


def _validate_entry_shape(entry: dict[str, object], index: int) -> list[ValidationIssue]:
    label = str(entry.get("path", f"assets[{index}]"))
    issues: list[ValidationIssue] = []
    missing = sorted(_REQUIRED_FIELDS - set(entry))
    if missing:
        issues.append(ValidationIssue(label, f"missing fields: {', '.join(missing)}"))
    relative_path = _safe_relative_path(entry.get("path"))
    if relative_path is None:
        issues.append(ValidationIssue(label, "path must be a safe non-empty relative path"))
    sha256 = entry.get("sha256")
    if not isinstance(sha256, str) or _SHA256_PATTERN.fullmatch(sha256) is None:
        issues.append(ValidationIssue(label, "sha256 must contain 64 lowercase hexadecimal digits"))
    size_bytes = entry.get("size_bytes")
    if not isinstance(size_bytes, int) or size_bytes < 0:
        issues.append(ValidationIssue(label, "size_bytes must be a non-negative integer"))
    if entry.get("contains_real_person") is not False:
        issues.append(ValidationIssue(label, "contains_real_person must be false"))
    if entry.get("contains_exif") is not False:
        issues.append(ValidationIssue(label, "contains_exif must be false for repository fixtures"))
    for field in ("media_type", "source", "license", "purpose"):
        value = entry.get(field)
        if not isinstance(value, str) or not value.strip():
            issues.append(ValidationIssue(label, f"{field} must be a non-empty string"))
    if not isinstance(entry.get("expected"), dict):
        issues.append(ValidationIssue(label, "expected must be a mapping"))
    return issues


def _validate_file(fixtures_root: Path, entry: dict[str, object]) -> list[ValidationIssue]:
    raw_path = entry.get("path")
    relative_path = _safe_relative_path(raw_path)
    if relative_path is None:
        return []
    label = relative_path.as_posix()
    target = fixtures_root / relative_path
    issues: list[ValidationIssue] = []
    if not target.is_file():
        return [ValidationIssue(label, "manifested asset does not exist")]
    expected_size = entry.get("size_bytes")
    if isinstance(expected_size, int) and target.stat().st_size != expected_size:
        issues.append(ValidationIssue(label, "file size does not match manifest"))
    expected_hash = entry.get("sha256")
    if isinstance(expected_hash, str) and _sha256(target) != expected_hash:
        issues.append(ValidationIssue(label, "SHA-256 does not match manifest"))
    if target.suffix.lower() in {".jpg", ".jpeg", ".tif", ".tiff"}:
        issues.append(
            ValidationIssue(
                label,
                "EXIF-capable fixture formats require a dedicated metadata audit",
            )
        )
    return issues


def validate_assets(fixtures_root: Path, manifest_path: Path) -> list[ValidationIssue]:
    data = load_manifest(manifest_path)
    issues = _validate_policy(data)
    entries = _manifest_entries(data)
    if not entries:
        issues.append(ValidationIssue("asset_manifest.yaml", "assets must contain entries"))
        return issues
    paths: list[str] = []
    for index, entry in enumerate(entries):
        issues.extend(_validate_entry_shape(entry, index))
        relative_path = _safe_relative_path(entry.get("path"))
        if relative_path is not None:
            paths.append(relative_path.as_posix())
        issues.extend(_validate_file(fixtures_root, entry))
    duplicates = sorted({path for path in paths if paths.count(path) > 1})
    for duplicate in duplicates:
        issues.append(ValidationIssue(duplicate, "duplicate manifest path"))
    manifested = set(paths)
    for target in sorted(fixtures_root.rglob("*")):
        if not target.is_file() or target.name in _IGNORED_NAMES:
            continue
        relative = target.relative_to(fixtures_root).as_posix()
        if relative not in manifested:
            issues.append(ValidationIssue(relative, "unmanifested fixture file"))
    return issues


def _parse_args() -> argparse.Namespace:
    project_root = Path(__file__).resolve().parents[1]
    default_root = project_root / "tests" / "fixtures"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures-root", type=Path, default=default_root)
    parser.add_argument("--manifest", type=Path, default=default_root / "asset_manifest.yaml")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    issues = validate_assets(args.fixtures_root.resolve(), args.manifest.resolve())
    if issues:
        for issue in issues:
            print(issue.render())
        raise SystemExit(1)
    print(f"Validated {args.manifest}")


if __name__ == "__main__":
    main()
