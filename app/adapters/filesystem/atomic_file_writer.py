from __future__ import annotations

import json
import os
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from app.adapters.filesystem.reparse_point_guard import assert_no_reparse_points

ReplaceFunction = Callable[[Path, Path], None]
ValidateFunction = Callable[[Path], None]


@dataclass(frozen=True)
class AtomicWriteResult:
    path: Path
    byte_size: int


class AtomicFileWriter:
    def __init__(
        self,
        managed_root: Path,
        *,
        replace: ReplaceFunction | None = None,
    ) -> None:
        self._managed_root = managed_root
        self._replace = replace or self._replace_path

    def write_bytes(
        self,
        target: Path,
        content: bytes,
        *,
        validate: ValidateFunction | None = None,
    ) -> AtomicWriteResult:
        assert_no_reparse_points(self._managed_root, target)
        target.parent.mkdir(parents=True, exist_ok=True)
        assert_no_reparse_points(self._managed_root, target)
        temporary = self._temporary_path(target)
        try:
            with temporary.open("wb") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            if validate is not None:
                validate(temporary)
            self._replace(temporary, target)
            self._sync_directory(target.parent)
            return AtomicWriteResult(path=target, byte_size=len(content))
        finally:
            temporary.unlink(missing_ok=True)

    def write_text(
        self,
        target: Path,
        content: str,
        *,
        validate: ValidateFunction | None = None,
    ) -> AtomicWriteResult:
        return self.write_bytes(target, content.encode("utf-8"), validate=validate)

    def write_json(
        self,
        target: Path,
        value: object,
        *,
        validate: ValidateFunction | None = None,
    ) -> AtomicWriteResult:
        content = json.dumps(
            value,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
        return self.write_text(target, content + "\n", validate=validate)

    @staticmethod
    def _replace_path(source: Path, destination: Path) -> None:
        os.replace(source, destination)

    @staticmethod
    def _temporary_path(target: Path) -> Path:
        descriptor, raw_path = tempfile.mkstemp(
            prefix=f".{target.name}.",
            suffix=".tmp",
            dir=target.parent,
        )
        os.close(descriptor)
        temporary = Path(raw_path)
        temporary.chmod(0o600)
        return temporary

    @staticmethod
    def _sync_directory(directory: Path) -> None:
        if os.name == "nt":
            return
        descriptor = os.open(directory, os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
