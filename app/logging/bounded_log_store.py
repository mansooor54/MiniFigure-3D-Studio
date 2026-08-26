from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path

from app.logging.redaction_policy import RedactionPolicy


@dataclass(frozen=True)
class RetentionResult:
    removed_files: tuple[str, ...]
    remaining_byte_size: int


class BoundedLogStore:
    def __init__(self, log_root: Path, policy: RedactionPolicy | None = None) -> None:
        self._log_root = log_root
        self._policy = policy or RedactionPolicy()

    def prune(
        self,
        *,
        retention_days: int,
        maximum_total_bytes: int,
        now_timestamp: float | None = None,
    ) -> RetentionResult:
        if retention_days < 0 or maximum_total_bytes < 0:
            raise ValueError("retention limits cannot be negative")
        if not self._log_root.exists():
            return RetentionResult(removed_files=(), remaining_byte_size=0)
        files = self._regular_log_files()
        now = time.time() if now_timestamp is None else now_timestamp
        cutoff = now - retention_days * 24 * 60 * 60
        removed: list[str] = []
        for path in list(files):
            if path.stat().st_mtime < cutoff:
                path.unlink()
                removed.append(path.name)
                files.remove(path)
        total = sum(path.stat().st_size for path in files)
        for path in sorted(files, key=lambda item: (item.stat().st_mtime, item.name)):
            if total <= maximum_total_bytes:
                break
            size = path.stat().st_size
            path.unlink()
            total -= size
            removed.append(path.name)
        return RetentionResult(
            removed_files=tuple(sorted(removed)),
            remaining_byte_size=total,
        )

    def read_excerpt(
        self,
        path: Path,
        *,
        maximum_entries: int = 100,
        maximum_bytes: int = 256 * 1024,
    ) -> tuple[dict[str, object], ...]:
        if maximum_entries <= 0 or maximum_bytes <= 0:
            raise ValueError("excerpt limits must be positive")
        if path.parent.resolve(strict=False) != self._log_root.resolve(strict=False):
            raise ValueError("log path must be a direct child of the log root")
        if path.is_symlink() or not path.is_file():
            raise ValueError("log path must be a regular file")
        data = self._tail_bytes(path, maximum_bytes)
        records: list[dict[str, object]] = []
        for line in data.splitlines()[-maximum_entries:]:
            try:
                payload = json.loads(line.decode("utf-8"))
            except (UnicodeError, json.JSONDecodeError):
                records.append(
                    {
                        "event_id": "logging.invalid_record",
                        "level": "warning",
                        "message": "A malformed log record was omitted.",
                        "fields": {},
                    }
                )
                continue
            if not isinstance(payload, dict):
                continue
            records.append(self._policy.redact_fields(payload))
        return tuple(records)

    def _regular_log_files(self) -> list[Path]:
        files: list[Path] = []
        for path in self._log_root.glob("*.jsonl*"):
            if path.is_symlink():
                raise ValueError("log retention refuses symbolic links")
            if path.is_file():
                files.append(path)
        return files

    @staticmethod
    def _tail_bytes(path: Path, maximum_bytes: int) -> bytes:
        size = path.stat().st_size
        with path.open("rb") as handle:
            if size > maximum_bytes:
                handle.seek(size - maximum_bytes)
                handle.readline()
            return handle.read(maximum_bytes)
