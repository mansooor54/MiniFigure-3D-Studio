from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from uuid import UUID, uuid4

from app.adapters.filesystem.reparse_point_guard import assert_no_reparse_points
from app.models.project import Project, ProjectLocale, ProjectMode
from app.ports.clock import Clock
from app.ports.project_repository import ProjectRepository, ProjectSummary

UuidFactory = Callable[[], UUID]


@dataclass(frozen=True)
class ProjectSession:
    project_root: Path
    project: Project


@dataclass(frozen=True)
class InventoryCategory:
    category: str
    file_count: int
    byte_size: int


class ProjectService:
    def __init__(
        self,
        repository: ProjectRepository,
        clock: Clock,
        *,
        uuid_factory: UuidFactory = uuid4,
    ) -> None:
        self._repository = repository
        self._clock = clock
        self._uuid_factory = uuid_factory

    def create_project(
        self,
        projects_root: Path,
        *,
        project_name: str,
        model_name: str,
        locale: ProjectLocale,
        mode: ProjectMode,
        permission_acknowledged: bool,
    ) -> ProjectSession:
        if not permission_acknowledged:
            raise ValueError("subject permission acknowledgment is required")
        project_id = self._uuid_factory()
        timestamp = self._clock.now()
        project = Project(
            project_id=project_id,
            project_name=project_name,
            model_name=model_name,
            locale=locale,
            mode=mode,
            created_at=timestamp,
            updated_at=timestamp,
            subject_permission_acknowledged_at=timestamp,
        )
        project_root = projects_root / f"project-{project_id.hex}"
        self._repository.create(project_root, project)
        return ProjectSession(project_root=project_root, project=project)

    def open_project(self, project_root: Path) -> ProjectSession:
        return ProjectSession(
            project_root=project_root,
            project=self._repository.load(project_root),
        )

    def rename_display_values(
        self,
        project_root: Path,
        *,
        project_name: str,
        model_name: str,
    ) -> Project:
        current = self._repository.load(project_root)
        updated = current.model_copy(
            update={
                "project_name": project_name,
                "model_name": model_name,
                "updated_at": self._clock.now(),
            }
        )
        validated = Project.model_validate(updated.model_dump(mode="python"))
        self._repository.commit(project_root, validated)
        return validated

    def list_recent_projects(self, projects_root: Path) -> tuple[ProjectSummary, ...]:
        return self._repository.list_projects(projects_root)

    def inventory(self, project_root: Path) -> tuple[InventoryCategory, ...]:
        project_root = project_root.resolve(strict=True)
        categories = (
            "inputs",
            "masks",
            "runs",
            "artifacts",
            "reports",
            "exports",
            "logs",
            ".staging",
        )
        results: list[InventoryCategory] = []
        for category in categories:
            root = project_root / category
            if not root.exists():
                continue
            assert_no_reparse_points(project_root, root)
            files = [path for path in root.rglob("*") if path.is_file()]
            for path in files:
                assert_no_reparse_points(project_root, path)
            results.append(
                InventoryCategory(
                    category=category,
                    file_count=len(files),
                    byte_size=sum(path.stat().st_size for path in files),
                )
            )
        return tuple(results)
