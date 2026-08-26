from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Protocol, runtime_checkable
from uuid import UUID

from app.models.project import Project


@dataclass(frozen=True)
class ProjectSummary:
    project_id: UUID
    project_name: str
    model_name: str
    project_root: Path
    updated_at: datetime
    recovery_required: bool


@dataclass(frozen=True)
class RecoveryCandidate:
    project_id: UUID
    project_root: Path
    run_id: UUID
    stage_id: str
    checkpoint_relative_path: str | None
    detected_at: datetime


@runtime_checkable
class ProjectRepository(Protocol):
    def create(self, project_root: Path, project: Project) -> None:
        """Create a new project workspace and initial committed manifest."""

    def load(self, project_root: Path) -> Project:
        """Load and validate the committed project manifest."""

    def commit(self, project_root: Path, project: Project) -> None:
        """Atomically replace the committed project manifest."""

    def list_projects(self, projects_root: Path) -> tuple[ProjectSummary, ...]:
        """Return validated project summaries in deterministic order."""

    def detect_recovery(self, project_root: Path) -> tuple[RecoveryCandidate, ...]:
        """Return abandoned runs that require an explicit recovery decision."""
