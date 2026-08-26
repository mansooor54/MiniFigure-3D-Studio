from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID

import pytest
from pydantic import ValidationError

from app.models.project import (
    CurrentArtifactSlot,
    Project,
    ProjectLocale,
    ProjectMode,
)

_NOW = datetime(2026, 1, 1, tzinfo=UTC)


def _project(**updates: object) -> Project:
    artifact_id = UUID(int=4)
    values: dict[str, object] = {
        "project_id": UUID(int=1),
        "project_name": "مشروع تجريبي",
        "model_name": "Mini Noor",
        "locale": ProjectLocale.ARABIC,
        "mode": ProjectMode.FAST_AI,
        "created_at": _NOW,
        "updated_at": _NOW + timedelta(seconds=1),
        "subject_permission_acknowledged_at": _NOW,
        "source_image_ids": (UUID(int=2),),
        "artifact_ids": (artifact_id,),
        "run_ids": (UUID(int=3),),
        "current_artifacts": (
            CurrentArtifactSlot(role="processed_mesh", artifact_id=artifact_id),
        ),
    }
    values.update(updates)
    return Project.model_validate(values)


def test_project_accepts_arabic_display_names() -> None:
    project = _project()
    assert project.project_name == "مشروع تجريبي"
    assert project.locale is ProjectLocale.ARABIC
    assert project.schema_version == 1


def test_project_requires_permission_within_timeline() -> None:
    with pytest.raises(ValidationError, match="permission acknowledgment"):
        _project(subject_permission_acknowledged_at=_NOW - timedelta(seconds=1))


def test_project_rejects_duplicate_artifact_references() -> None:
    with pytest.raises(ValidationError, match="artifact_ids must be unique"):
        _project(artifact_ids=(UUID(int=4), UUID(int=4)))


def test_project_rejects_current_uncommitted_artifact() -> None:
    with pytest.raises(ValidationError, match="committed artifact_ids"):
        _project(
            current_artifacts=(
                CurrentArtifactSlot(role="processed_mesh", artifact_id=UUID(int=99)),
            )
        )


def test_project_rejects_control_characters_in_display_name() -> None:
    with pytest.raises(ValidationError, match="control characters"):
        _project(project_name="bad\nname")
