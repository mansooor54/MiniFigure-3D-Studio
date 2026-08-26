from __future__ import annotations

from pathlib import Path

from app.adapters.filesystem.atomic_file_writer import AtomicFileWriter
from app.adapters.filesystem.safe_paths import (
    project_relative_path,
    resolve_project_child,
    safe_display_filename,
)


def test_arabic_project_and_filename_round_trip(tmp_path: Path) -> None:
    root = tmp_path / "مشروع تمثال مصغر"
    target = resolve_project_child(root, "inputs/metadata/وصف الصورة.json")
    AtomicFileWriter(root).write_text(target, '{"الواجهة": "أمامية"}\n')
    assert target.read_text(encoding="utf-8") == '{"الواجهة": "أمامية"}\n'
    assert project_relative_path(root, target) == "inputs/metadata/وصف الصورة.json"


def test_quotes_and_windows_characters_are_sanitized() -> None:
    filename = safe_display_filename(
        'اسم "النموذج" <الأول>',
        fallback="model",
        extension="glb",
    )
    assert filename == "اسم -النموذج- -الأول-.glb"


def test_long_but_portable_relative_path_round_trip(tmp_path: Path) -> None:
    root = tmp_path / "مشروع"
    relative = "/".join(
        (
            "runs",
            "مرحلة-" + "\u0627" * 70,
            "نتائج-" + "\u0628" * 70,
            "result.json",
        )
    )
    target = resolve_project_child(root, relative)
    AtomicFileWriter(root).write_json(target, {"status": "succeeded"})
    assert project_relative_path(root, target) == relative
