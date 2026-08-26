from __future__ import annotations

from pathlib import Path

import pytest

from app.adapters.filesystem.reparse_point_guard import (
    ReparsePointError,
    assert_no_reparse_points,
    is_reparse_point,
    require_regular_file,
)


def test_regular_managed_file_passes_guard(tmp_path: Path) -> None:
    root = tmp_path / "project"
    target = root / "artifacts" / "model.glb"
    target.parent.mkdir(parents=True)
    target.write_bytes(b"glb")
    assert_no_reparse_points(root, target)
    require_regular_file(root, target)


def test_candidate_outside_root_is_rejected(tmp_path: Path) -> None:
    root = tmp_path / "project"
    outside = tmp_path / "outside.txt"
    root.mkdir()
    outside.write_text("outside", encoding="utf-8")
    with pytest.raises(ReparsePointError, match="outside"):
        assert_no_reparse_points(root, outside)


def test_symlink_component_is_rejected(tmp_path: Path) -> None:
    root = tmp_path / "project"
    outside = tmp_path / "outside"
    root.mkdir()
    outside.mkdir()
    link = root / "linked"
    try:
        link.symlink_to(outside, target_is_directory=True)
    except OSError as error:
        pytest.skip(f"symlink creation is unavailable: {error}")
    assert is_reparse_point(link)
    with pytest.raises(ReparsePointError, match="reparse point"):
        assert_no_reparse_points(root, link / "model.glb")


def test_leaf_symlink_is_rejected(tmp_path: Path) -> None:
    root = tmp_path / "project"
    root.mkdir()
    original = root / "original.txt"
    original.write_text("data", encoding="utf-8")
    link = root / "link.txt"
    try:
        link.symlink_to(original)
    except OSError as error:
        pytest.skip(f"symlink creation is unavailable: {error}")
    with pytest.raises(ReparsePointError):
        require_regular_file(root, link)
