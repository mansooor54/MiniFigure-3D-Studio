from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

import pytest

from app.adapters.filesystem.local_project_repository import LocalProjectRepository
from app.application.orchestration.recovery_coordinator import (
    RecoveryAction,
    RecoveryCoordinator,
)
from app.models.project import Project, ProjectLocale, ProjectMode
from app.workers.checkpoint_manager import CheckpointManager


@dataclass(frozen=True)
class FixedClock:
    value: datetime

    def now(self) -> datetime:
        return self.value


def _setup(tmp_path: Path) -> tuple[Path, LocalProjectRepository, FixedClock]:
    clock = FixedClock(datetime(2026, 1, 1, tzinfo=UTC))
    repository = LocalProjectRepository(clock)
    project = Project(
        project_id=UUID(int=1),
        project_name="Project",
        model_name="Model",
        locale=ProjectLocale.ENGLISH,
        mode=ProjectMode.FAST_AI,
        created_at=clock.value,
        updated_at=clock.value,
        subject_permission_acknowledged_at=clock.value,
    )
    root = tmp_path / "project"
    repository.create(root, project)
    repository.append_journal_event(
        root,
        {
            "event_type": "run_started",
            "project_id": str(project.project_id),
            "run_id": str(UUID(int=2)),
            "stage_id": "shape_generation",
            "recorded_at": clock.value.isoformat(),
        },
    )
    return root, repository, clock


def test_run_without_checkpoint_cannot_resume(tmp_path: Path) -> None:
    root, repository, clock = _setup(tmp_path)
    coordinator = RecoveryCoordinator(repository, repository, clock)
    plan = coordinator.inspect(root)[0]
    assert plan.checkpoint_valid is False
    assert RecoveryAction.RESUME_FROM_CHECKPOINT not in plan.allowed_actions
    with pytest.raises(ValueError, match="not valid"):
        coordinator.select(plan, RecoveryAction.RESUME_FROM_CHECKPOINT)


def test_valid_checkpoint_enables_resume_and_terminal_event_clears_run(
    tmp_path: Path,
) -> None:
    root, repository, clock = _setup(tmp_path)
    CheckpointManager(root, repository, clock).register(
        checkpoint_id=UUID(int=3),
        project_id=UUID(int=1),
        run_id=UUID(int=2),
        stage_id="shape_generation",
        state={"completed_units": 5},
    )
    coordinator = RecoveryCoordinator(repository, repository, clock)
    plan = coordinator.inspect(root)[0]
    assert plan.checkpoint_valid is True
    assert RecoveryAction.RESUME_FROM_CHECKPOINT in plan.allowed_actions
    coordinator.select(plan, RecoveryAction.RESUME_FROM_CHECKPOINT)
    assert len(repository.detect_recovery(root)) == 1
    coordinator.mark_terminal(plan, terminal_status="cancelled")
    assert repository.detect_recovery(root) == ()


def test_mark_failed_action_closes_abandoned_run(tmp_path: Path) -> None:
    root, repository, clock = _setup(tmp_path)
    coordinator = RecoveryCoordinator(repository, repository, clock)
    plan = coordinator.inspect(root)[0]
    coordinator.select(plan, RecoveryAction.MARK_RUN_FAILED)
    assert repository.detect_recovery(root) == ()
