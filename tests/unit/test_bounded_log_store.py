from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from app.logging.bounded_log_store import BoundedLogStore


def _write_record(path: Path, event_id: str, message: str) -> None:
    path.write_text(
        json.dumps(
            {
                "event_id": event_id,
                "level": "info",
                "message": message,
                "fields": {},
            }
        )
        + "\n",
        encoding="utf-8",
    )


def test_prune_removes_expired_and_oldest_over_limit(tmp_path: Path) -> None:
    old = tmp_path / "application.jsonl.2"
    middle = tmp_path / "application.jsonl.1"
    current = tmp_path / "application.jsonl"
    for path, content in ((old, "old"), (middle, "middle"), (current, "current")):
        path.write_text(content, encoding="utf-8")
    now = 2_000_000_000.0
    os.utime(old, (now - 20 * 86400, now - 20 * 86400))
    os.utime(middle, (now - 100, now - 100))
    os.utime(current, (now, now))
    result = BoundedLogStore(tmp_path).prune(
        retention_days=14,
        maximum_total_bytes=current.stat().st_size,
        now_timestamp=now,
    )
    assert result.removed_files == tuple(sorted((old.name, middle.name)))
    assert current.exists()
    assert result.remaining_byte_size == current.stat().st_size


def test_read_excerpt_returns_safe_tail_and_substitutes_malformed_line(
    tmp_path: Path,
) -> None:
    path = tmp_path / "application.jsonl"
    secret = "sk-" + "q" * 24
    lines = [
        json.dumps({"event_id": "one", "message": "safe", "fields": {}}),
        "not-json",
        json.dumps(
            {"event_id": "two", "message": "done", "fields": {"api_key": secret}}
        ),
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    excerpt = BoundedLogStore(tmp_path).read_excerpt(
        path,
        maximum_entries=2,
        maximum_bytes=4096,
    )
    encoded = json.dumps(excerpt)
    assert secret not in encoded
    assert excerpt[0]["event_id"] == "logging.invalid_record"
    assert excerpt[1]["event_id"] == "two"


def test_read_excerpt_rejects_nested_or_symlink_log(tmp_path: Path) -> None:
    nested = tmp_path / "nested" / "application.jsonl"
    nested.parent.mkdir()
    _write_record(nested, "nested", "not allowed")
    store = BoundedLogStore(tmp_path)
    with pytest.raises(ValueError, match="direct child"):
        store.read_excerpt(nested)
    target = tmp_path / "target.jsonl"
    _write_record(target, "target", "safe")
    link = tmp_path / "link.jsonl"
    try:
        link.symlink_to(target)
    except OSError as error:
        pytest.skip(f"symlink creation is unavailable: {error}")
    with pytest.raises(ValueError, match="regular file"):
        store.read_excerpt(link)
