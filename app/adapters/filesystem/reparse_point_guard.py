from __future__ import annotations

import os
import stat
from pathlib import Path

from app.adapters.filesystem.safe_paths import PathSecurityError


class ReparsePointError(PathSecurityError):
    """Raised when a managed operation encounters a symlink or Windows reparse point."""


def is_reparse_point(path: Path) -> bool:
    if path.is_symlink():
        return True
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        return False
    attributes = getattr(metadata, "st_file_attributes", 0)
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return bool(attributes & reparse_flag)


def assert_no_reparse_points(
    managed_root: Path,
    candidate: Path,
    *,
    include_leaf: bool = True,
) -> None:
    root = Path(os.path.abspath(managed_root))
    target = Path(os.path.abspath(candidate))
    try:
        relative = target.relative_to(root)
    except ValueError as error:
        raise ReparsePointError("candidate is outside the managed root") from error
    paths = [root]
    current = root
    for part in relative.parts:
        current = current / part
        paths.append(current)
    if not include_leaf and len(paths) > 1:
        paths.pop()
    for path in paths:
        if path.exists() and is_reparse_point(path):
            raise ReparsePointError(f"reparse point is not allowed: {path.name}")


def require_regular_file(managed_root: Path, candidate: Path) -> None:
    assert_no_reparse_points(managed_root, candidate)
    if not candidate.is_file():
        raise ReparsePointError("candidate is not a regular file")
