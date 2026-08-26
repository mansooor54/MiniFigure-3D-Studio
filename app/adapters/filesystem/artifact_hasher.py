from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from app.adapters.filesystem.reparse_point_guard import (
    ReparsePointError,
    assert_no_reparse_points,
)


class ArtifactTooLargeError(ValueError):
    """Raised when hashing would exceed the caller's declared size limit."""


@dataclass(frozen=True)
class HashResult:
    sha256: str
    byte_size: int
    file_count: int


class ArtifactHasher:
    def __init__(self, managed_root: Path, *, chunk_size: int = 1024 * 1024) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        self._managed_root = managed_root
        self._chunk_size = chunk_size

    def hash_file(self, path: Path, *, maximum_bytes: int | None = None) -> HashResult:
        assert_no_reparse_points(self._managed_root, path)
        if not path.is_file():
            raise FileNotFoundError(path)
        size = path.stat().st_size
        self._check_limit(size, maximum_bytes)
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(self._chunk_size), b""):
                digest.update(chunk)
        return HashResult(sha256=digest.hexdigest(), byte_size=size, file_count=1)

    def hash_directory(
        self,
        path: Path,
        *,
        maximum_bytes: int | None = None,
    ) -> HashResult:
        assert_no_reparse_points(self._managed_root, path)
        if not path.is_dir():
            raise NotADirectoryError(path)
        digest = hashlib.sha256()
        total_size = 0
        file_count = 0
        for child in sorted(path.rglob("*"), key=lambda item: item.relative_to(path).as_posix()):
            if child.is_symlink():
                raise ReparsePointError("artifact directory contains a symbolic link")
            if not child.is_file():
                continue
            assert_no_reparse_points(self._managed_root, child)
            relative = child.relative_to(path).as_posix().encode("utf-8")
            size = child.stat().st_size
            total_size += size
            self._check_limit(total_size, maximum_bytes)
            digest.update(len(relative).to_bytes(8, byteorder="big"))
            digest.update(relative)
            digest.update(size.to_bytes(8, byteorder="big"))
            with child.open("rb") as handle:
                for chunk in iter(lambda: handle.read(self._chunk_size), b""):
                    digest.update(chunk)
            file_count += 1
        return HashResult(
            sha256=digest.hexdigest(),
            byte_size=total_size,
            file_count=file_count,
        )

    @staticmethod
    def _check_limit(current_size: int, maximum_bytes: int | None) -> None:
        if maximum_bytes is not None and current_size > maximum_bytes:
            raise ArtifactTooLargeError("artifact exceeds the declared byte limit")
