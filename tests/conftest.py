from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Callable, Iterator
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

import pytest

_FIXED_TIME = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
_PREVIOUS_QT_PLATFORM = os.environ.get("QT_QPA_PLATFORM")
_PREVIOUS_QT_PLUGIN_PATH = os.environ.get("QT_PLUGIN_PATH")


def _prepare_qt_environment() -> None:
    import PySide6

    plugin_root = Path(PySide6.__file__).parent / "Qt" / "plugins"
    if sys.platform == "darwin":
        subprocess.run(
            ["chflags", "-R", "nohidden", str(plugin_root)],
            check=True,
            capture_output=True,
            text=True,
        )
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    os.environ["QT_PLUGIN_PATH"] = str(plugin_root)


_prepare_qt_environment()


@pytest.fixture
def fixed_clock() -> Callable[[], datetime]:
    return lambda: _FIXED_TIME


@pytest.fixture
def deterministic_id_factory() -> Callable[[], UUID]:
    counter = 0

    def create_id() -> UUID:
        nonlocal counter
        counter += 1
        return UUID(int=counter)

    return create_id


@pytest.fixture
def project_root(tmp_path: Path) -> Path:
    root = tmp_path / "مشروع MiniFigure"
    root.mkdir()
    return root


@pytest.fixture(scope="session", autouse=True)
def qt_environment() -> Iterator[None]:
    yield
    _restore_environment("QT_QPA_PLATFORM", _PREVIOUS_QT_PLATFORM)
    _restore_environment("QT_PLUGIN_PATH", _PREVIOUS_QT_PLUGIN_PATH)


def _restore_environment(name: str, value: str | None) -> None:
    if value is None:
        os.environ.pop(name, None)
    else:
        os.environ[name] = value


@pytest.fixture(scope="session")
def qapp_args() -> list[str]:
    return ["minifigure-tests"]
