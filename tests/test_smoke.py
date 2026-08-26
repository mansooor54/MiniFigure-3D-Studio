from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

from PySide6.QtWidgets import QApplication, QLabel


def test_fixed_clock_is_timezone_aware(
    fixed_clock: Callable[[], datetime],
) -> None:
    assert fixed_clock() == datetime(2026, 1, 1, 12, 0, tzinfo=UTC)


def test_deterministic_ids_are_stable(
    deterministic_id_factory: Callable[[], UUID],
) -> None:
    assert deterministic_id_factory() == UUID(int=1)
    assert deterministic_id_factory() == UUID(int=2)


def test_project_root_supports_arabic(project_root: Path) -> None:
    target = project_root / "ملف اختبار.txt"
    target.write_text("MiniFigure", encoding="utf-8")
    assert target.read_text(encoding="utf-8") == "MiniFigure"


def test_qt_application_processes_a_widget(qapp: QApplication) -> None:
    label = QLabel("MiniFigure 3D Studio")
    label.resize(320, 80)
    label.show()
    qapp.processEvents()
    assert label.size().width() == 320
    label.close()
