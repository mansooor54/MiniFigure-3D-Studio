from __future__ import annotations

from pathlib import Path
from typing import Final

import yaml

_ROOT: Final[Path] = Path(__file__).resolve().parents[2]


def _workflow() -> dict[object, object]:
    path = _ROOT / ".github" / "workflows" / "quality.yml"
    content = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(content, dict)
    return content


def test_workflow_uses_read_only_repository_permissions() -> None:
    workflow = _workflow()
    permissions = workflow["permissions"]
    assert isinstance(permissions, dict)
    assert permissions == {"contents": "read"}


def test_workflow_has_portable_python_matrix() -> None:
    workflow = _workflow()
    jobs = workflow["jobs"]
    assert isinstance(jobs, dict)
    job = jobs["portable-quality"]
    assert isinstance(job, dict)
    strategy = job["strategy"]
    assert isinstance(strategy, dict)
    matrix = strategy["matrix"]
    assert isinstance(matrix, dict)
    assert matrix["os"] == ["ubuntu-latest", "macos-latest"]


def test_workflow_does_not_use_privileged_pull_request_target() -> None:
    workflow = _workflow()
    triggers = workflow.get("on", workflow.get(True))
    assert isinstance(triggers, dict)
    assert "pull_request" in triggers
    assert "pull_request_target" not in triggers
