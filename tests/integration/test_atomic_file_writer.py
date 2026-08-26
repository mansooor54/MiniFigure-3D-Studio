from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.adapters.filesystem.atomic_file_writer import AtomicFileWriter
from app.adapters.filesystem.reparse_point_guard import ReparsePointError


def _temporary_files(parent: Path, target_name: str) -> list[Path]:
    return list(parent.glob(f".{target_name}.*.tmp"))


def test_atomic_writer_replaces_existing_file(tmp_path: Path) -> None:
    root = tmp_path / "project"
    target = root / "project.json"
    root.mkdir()
    target.write_text("old", encoding="utf-8")
    result = AtomicFileWriter(root).write_text(target, "new")
    assert result.byte_size == 3
    assert target.read_text(encoding="utf-8") == "new"
    assert _temporary_files(root, target.name) == []


def test_atomic_json_is_deterministic_and_validated(tmp_path: Path) -> None:
    root = tmp_path / "project"
    target = root / "project.json"

    def validate(path: Path) -> None:
        assert json.loads(path.read_text(encoding="utf-8")) == {"a": 1, "b": 2}

    AtomicFileWriter(root).write_json(target, {"b": 2, "a": 1}, validate=validate)
    assert target.read_text(encoding="utf-8") == '{\n  "a": 1,\n  "b": 2\n}\n'


def test_validation_failure_preserves_prior_file_and_cleans_temporary(
    tmp_path: Path,
) -> None:
    root = tmp_path / "project"
    target = root / "project.json"
    root.mkdir()
    target.write_text("committed", encoding="utf-8")

    def reject(_path: Path) -> None:
        raise ValueError("seeded validation failure")

    with pytest.raises(ValueError, match="seeded validation failure"):
        AtomicFileWriter(root).write_text(target, "candidate", validate=reject)
    assert target.read_text(encoding="utf-8") == "committed"
    assert _temporary_files(root, target.name) == []


def test_replace_failure_preserves_prior_file_and_cleans_temporary(tmp_path: Path) -> None:
    root = tmp_path / "project"
    target = root / "project.json"
    root.mkdir()
    target.write_text("committed", encoding="utf-8")

    def fail_replace(_source: Path, _destination: Path) -> None:
        raise OSError("seeded replace failure")

    writer = AtomicFileWriter(root, replace=fail_replace)
    with pytest.raises(OSError, match="seeded replace failure"):
        writer.write_text(target, "candidate")
    assert target.read_text(encoding="utf-8") == "committed"
    assert _temporary_files(root, target.name) == []


def test_atomic_writer_rejects_outside_target_before_creating_parent(tmp_path: Path) -> None:
    root = tmp_path / "project"
    outside = tmp_path / "outside" / "file.txt"
    with pytest.raises(ReparsePointError, match="outside"):
        AtomicFileWriter(root).write_text(outside, "forbidden")
    assert not outside.parent.exists()
