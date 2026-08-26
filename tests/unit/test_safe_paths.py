from __future__ import annotations

from pathlib import Path
from uuid import UUID

import pytest

from app.adapters.filesystem.safe_paths import (
    PathSecurityError,
    generated_name,
    project_relative_path,
    resolve_project_child,
    safe_display_filename,
)


def test_safe_display_filename_preserves_arabic_and_replaces_windows_characters() -> None:
    result = safe_display_filename(
        " صورة: أمامية?.jpg ",
        fallback="image",
        extension="png",
    )
    assert result == "صورة- أمامية-.png"


def test_safe_display_filename_escapes_windows_reserved_name() -> None:
    assert safe_display_filename("CON", fallback="image", extension="jpg") == "_CON.jpg"


def test_generated_name_is_stable_and_portable() -> None:
    result = generated_name("source-image", UUID(int=1), "png")
    assert result == "source-image-00000000000000000000000000000001.png"


def test_resolve_project_child_accepts_arabic_and_spaces(tmp_path: Path) -> None:
    root = tmp_path / "مشروع"
    root.mkdir()
    child = resolve_project_child(root, "inputs/originals/صورة أمامية.png")
    assert child == root / "inputs" / "originals" / "صورة أمامية.png"


@pytest.mark.parametrize(
    "relative_path",
    (
        "../outside.txt",
        "inputs/../../outside.txt",
        "/absolute.txt",
        "C:/windows.txt",
        "inputs\\windows.txt",
        "inputs/./file.txt",
    ),
)
def test_resolve_project_child_rejects_nonportable_or_escaping_path(
    tmp_path: Path,
    relative_path: str,
) -> None:
    with pytest.raises(PathSecurityError):
        resolve_project_child(tmp_path, relative_path)


def test_project_relative_path_round_trips(tmp_path: Path) -> None:
    root = tmp_path / "project"
    target = root / "artifacts" / "processed" / "model.glb"
    target.parent.mkdir(parents=True)
    target.write_bytes(b"glb")
    assert project_relative_path(root, target) == "artifacts/processed/model.glb"


def test_existing_symlink_escape_is_rejected(tmp_path: Path) -> None:
    root = tmp_path / "project"
    outside = tmp_path / "outside"
    root.mkdir()
    outside.mkdir()
    link = root / "linked"
    try:
        link.symlink_to(outside, target_is_directory=True)
    except OSError as error:
        pytest.skip(f"symlink creation is unavailable: {error}")
    with pytest.raises(PathSecurityError):
        resolve_project_child(root, "linked/file.txt")
