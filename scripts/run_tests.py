from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import PySide6


def prepare_qt_test_environment() -> Path:
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
    return plugin_root


def main() -> int:
    prepare_qt_test_environment()
    import pytest

    return pytest.main(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
