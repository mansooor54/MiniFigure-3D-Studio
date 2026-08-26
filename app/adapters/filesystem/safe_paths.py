from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Final
from uuid import UUID

_INVALID_WINDOWS_CHARACTERS: Final[re.Pattern[str]] = re.compile(r"[<>:\"/\\|?*\x00-\x1f]")
_WHITESPACE: Final[re.Pattern[str]] = re.compile(r"\s+")
_RESERVED_WINDOWS_NAMES: Final[frozenset[str]] = frozenset(
    {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        *(f"COM{index}" for index in range(1, 10)),
        *(f"LPT{index}" for index in range(1, 10)),
    }
)


class PathSecurityError(ValueError):
    """Raised when a requested path could escape or alias managed storage."""


@dataclass(frozen=True)
class SafePathPolicy:
    maximum_segment_length: int = 120
    maximum_relative_length: int = 512


_DEFAULT_POLICY: Final[SafePathPolicy] = SafePathPolicy()


def safe_display_filename(
    display_name: str,
    *,
    fallback: str,
    extension: str | None = None,
    policy: SafePathPolicy = _DEFAULT_POLICY,
) -> str:
    normalized = unicodedata.normalize("NFKC", display_name)
    normalized = _INVALID_WINDOWS_CHARACTERS.sub("-", normalized)
    normalized = _WHITESPACE.sub(" ", normalized).strip(" .")
    if not normalized:
        normalized = fallback
    stem = Path(normalized).stem.strip(" .") or fallback
    if stem.upper() in _RESERVED_WINDOWS_NAMES:
        stem = f"_{stem}"
    suffix = _normalize_extension(extension)
    maximum_stem = policy.maximum_segment_length - len(suffix)
    stem = stem[:maximum_stem].rstrip(" .") or fallback[:maximum_stem]
    return f"{stem}{suffix}"


def generated_name(prefix: str, identifier: UUID, extension: str) -> str:
    safe_prefix = safe_display_filename(prefix, fallback="item", extension=None)
    suffix = _normalize_extension(extension)
    return f"{safe_prefix}-{identifier.hex}{suffix}"


def resolve_project_child(
    project_root: Path,
    relative_path: str,
    *,
    policy: SafePathPolicy = _DEFAULT_POLICY,
) -> Path:
    portable = _validate_relative_path(relative_path, policy)
    root = project_root.resolve(strict=False)
    candidate = root.joinpath(*portable.parts).resolve(strict=False)
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise PathSecurityError("path escapes the project root") from error
    _reject_symlink_components(root, candidate)
    return candidate


def project_relative_path(project_root: Path, candidate: Path) -> str:
    root = project_root.resolve(strict=False)
    resolved = candidate.resolve(strict=False)
    try:
        relative = resolved.relative_to(root)
    except ValueError as error:
        raise PathSecurityError("path is outside the project root") from error
    _reject_symlink_components(root, resolved)
    return relative.as_posix()


def require_managed_file(project_root: Path, relative_path: str) -> Path:
    candidate = resolve_project_child(project_root, relative_path)
    if not candidate.is_file():
        raise PathSecurityError("managed file does not exist")
    return candidate


def _validate_relative_path(relative_path: str, policy: SafePathPolicy) -> PurePosixPath:
    if not relative_path or len(relative_path) > policy.maximum_relative_length:
        raise PathSecurityError("relative path has an invalid length")
    if "\\" in relative_path or ":" in relative_path or "\x00" in relative_path:
        raise PathSecurityError("relative path is not portable")
    raw_parts = relative_path.split("/")
    if any(part in {"", ".", ".."} for part in raw_parts):
        raise PathSecurityError("relative path must stay inside the project")
    portable = PurePosixPath(relative_path)
    if portable.is_absolute():
        raise PathSecurityError("relative path must stay inside the project")
    if any(len(part) > policy.maximum_segment_length for part in portable.parts):
        raise PathSecurityError("relative path contains an oversized segment")
    return portable


def _normalize_extension(extension: str | None) -> str:
    if extension is None or extension == "":
        return ""
    suffix = extension if extension.startswith(".") else f".{extension}"
    if re.fullmatch(r"\.[A-Za-z0-9]{1,12}", suffix) is None:
        raise PathSecurityError("extension must be alphanumeric")
    return suffix.lower()


def _reject_symlink_components(root: Path, candidate: Path) -> None:
    relative = candidate.relative_to(root)
    current = root
    for part in relative.parts:
        current = current / part
        if current.exists() and current.is_symlink():
            raise PathSecurityError("managed paths cannot traverse symbolic links")
