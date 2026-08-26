from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from app.adapters.filesystem.artifact_hasher import ArtifactHasher, ArtifactTooLargeError
from app.adapters.filesystem.reparse_point_guard import ReparsePointError


def test_file_hash_matches_sha256(tmp_path: Path) -> None:
    root = tmp_path / "project"
    target = root / "artifacts" / "model.bin"
    target.parent.mkdir(parents=True)
    content = b"MiniFigure artifact"
    target.write_bytes(content)
    result = ArtifactHasher(root, chunk_size=4).hash_file(target)
    assert result.sha256 == hashlib.sha256(content).hexdigest()
    assert result.byte_size == len(content)
    assert result.file_count == 1


def test_file_hash_enforces_declared_limit(tmp_path: Path) -> None:
    root = tmp_path / "project"
    target = root / "large.bin"
    root.mkdir()
    target.write_bytes(b"12345")
    with pytest.raises(ArtifactTooLargeError):
        ArtifactHasher(root).hash_file(target, maximum_bytes=4)


def test_directory_hash_is_deterministic_and_path_sensitive(tmp_path: Path) -> None:
    root = tmp_path / "project"
    first = root / "first"
    second = root / "second"
    for directory in (first, second):
        directory.mkdir(parents=True)
        (directory / "a.txt").write_text("A", encoding="utf-8")
        (directory / "b.txt").write_text("B", encoding="utf-8")
    hasher = ArtifactHasher(root)
    assert hasher.hash_directory(first) == hasher.hash_directory(second)
    (second / "b.txt").rename(second / "c.txt")
    assert hasher.hash_directory(first).sha256 != hasher.hash_directory(second).sha256


def test_directory_hash_rejects_symlink(tmp_path: Path) -> None:
    root = tmp_path / "project"
    artifact = root / "artifact"
    artifact.mkdir(parents=True)
    original = artifact / "original.txt"
    original.write_text("data", encoding="utf-8")
    link = artifact / "link.txt"
    try:
        link.symlink_to(original)
    except OSError as error:
        pytest.skip(f"symlink creation is unavailable: {error}")
    with pytest.raises(ReparsePointError):
        ArtifactHasher(root).hash_directory(artifact)


def test_directory_hash_enforces_aggregate_limit(tmp_path: Path) -> None:
    root = tmp_path / "project"
    artifact = root / "artifact"
    artifact.mkdir(parents=True)
    (artifact / "a.bin").write_bytes(b"123")
    (artifact / "b.bin").write_bytes(b"456")
    with pytest.raises(ArtifactTooLargeError):
        ArtifactHasher(root).hash_directory(artifact, maximum_bytes=5)
