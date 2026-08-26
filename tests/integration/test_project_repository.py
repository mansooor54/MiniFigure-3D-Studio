from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import UUID

import pytest

from app.adapters.filesystem.local_project_repository import (
    LocalProjectRepository,
    ProjectCorruptError,
    UnsupportedProjectSchemaError,
)
from app.config.paths import ProjectLayout
from app.models.project import Project, ProjectLocale, ProjectMode


@dataclass(frozen=True)
class FixedClock:
    value: datetime

    def now(self) -> datetime:
        return self.value


def _project(project_id: int = 1, *, updated_offset: int = 0) -> Project:
    created = datetime(2026, 1, 1, tzinfo=UTC)
    return Project(
        project_id=UUID(int=project_id),
        project_name=f"مشروع {project_id}",
        model_name=f"Model {project_id}",
        locale=ProjectLocale.ARABIC,
        mode=ProjectMode.FAST_AI,
        created_at=created,
        updated_at=created + timedelta(seconds=updated_offset),
        subject_permission_acknowledged_at=created,
    )


def _repository() -> LocalProjectRepository:
    return LocalProjectRepository(FixedClock(datetime(2026, 1, 2, tzinfo=UTC)))


def test_create_load_and_commit_project_manifest(tmp_path: Path) -> None:
    root = tmp_path / "project-1"
    repository = _repository()
    repository.create(root, _project())
    layout = ProjectLayout(root)
    assert all(path.is_dir() for path in layout.managed_directories())
    assert repository.load(root) == _project()
    updated = _project().model_copy(
        update={
            "project_name": "اسم جديد",
            "updated_at": datetime(2026, 1, 2, tzinfo=UTC),
        }
    )
    repository.commit(root, Project.model_validate(updated.model_dump()))
    assert repository.load(root).project_name == "اسم جديد"
    assert len(layout.journal.read_text(encoding="utf-8").splitlines()) == 2


def test_list_projects_is_newest_first_and_marks_recovery(tmp_path: Path) -> None:
    repository = _repository()
    first_root = tmp_path / "first"
    second_root = tmp_path / "second"
    repository.create(first_root, _project(1, updated_offset=1))
    repository.create(second_root, _project(2, updated_offset=2))
    repository.append_journal_event(
        second_root,
        {
            "event_type": "run_started",
            "project_id": str(UUID(int=2)),
            "run_id": str(UUID(int=10)),
            "stage_id": "shape_generation",
            "recorded_at": datetime(2026, 1, 2, tzinfo=UTC).isoformat(),
        },
    )
    summaries = repository.list_projects(tmp_path)
    assert [summary.project_id for summary in summaries] == [UUID(int=2), UUID(int=1)]
    assert summaries[0].recovery_required is True
    assert summaries[1].recovery_required is False


def test_corrupt_manifest_is_rejected(tmp_path: Path) -> None:
    root = tmp_path / "project"
    root.mkdir()
    (root / "project.json").write_text("not json", encoding="utf-8")
    with pytest.raises(ProjectCorruptError, match="cannot be decoded"):
        _repository().load(root)


def test_future_schema_is_rejected_truthfully(tmp_path: Path) -> None:
    root = tmp_path / "project"
    repository = _repository()
    repository.create(root, _project())
    manifest = json.loads((root / "project.json").read_text(encoding="utf-8"))
    manifest["schema_version"] = 2
    (root / "project.json").write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(UnsupportedProjectSchemaError, match="schema version"):
        repository.load(root)


def test_terminal_event_clears_recovery_candidate(tmp_path: Path) -> None:
    root = tmp_path / "project"
    repository = _repository()
    repository.create(root, _project())
    run_id = UUID(int=10)
    base_event = {
        "project_id": str(UUID(int=1)),
        "run_id": str(run_id),
        "stage_id": "shape_generation",
        "recorded_at": datetime(2026, 1, 2, tzinfo=UTC).isoformat(),
    }
    repository.append_journal_event(root, {**base_event, "event_type": "run_started"})
    assert len(repository.detect_recovery(root)) == 1
    repository.append_journal_event(root, {**base_event, "event_type": "run_terminal"})
    assert repository.detect_recovery(root) == ()
