from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

import pytest

from app.adapters.filesystem.local_project_repository import LocalProjectRepository
from app.models.project import ProjectLocale, ProjectMode
from app.services.project_service import ProjectService


@dataclass(frozen=True)
class FixedClock:
    value: datetime

    def now(self) -> datetime:
        return self.value


def _service() -> ProjectService:
    clock = FixedClock(datetime(2026, 1, 1, tzinfo=UTC))
    repository = LocalProjectRepository(clock)
    return ProjectService(repository, clock, uuid_factory=lambda: UUID(int=1))


def test_project_creation_requires_permission_acknowledgment(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="permission acknowledgment"):
        _service().create_project(
            tmp_path,
            project_name="Project",
            model_name="Model",
            locale=ProjectLocale.ENGLISH,
            mode=ProjectMode.FAST_AI,
            permission_acknowledged=False,
        )


def test_project_creation_uses_uuid_path_not_display_name(tmp_path: Path) -> None:
    session = _service().create_project(
        tmp_path,
        project_name="مشروع / unsafe",
        model_name="Mini Noor",
        locale=ProjectLocale.ARABIC,
        mode=ProjectMode.FAST_AI,
        permission_acknowledged=True,
    )
    assert session.project_root.name == f"project-{UUID(int=1).hex}"
    assert session.project.project_name == "مشروع / unsafe"
    assert session.project_root.is_dir()


def test_rename_changes_display_values_not_workspace_path(tmp_path: Path) -> None:
    service = _service()
    session = service.create_project(
        tmp_path,
        project_name="Old",
        model_name="Old Model",
        locale=ProjectLocale.ENGLISH,
        mode=ProjectMode.FAST_AI,
        permission_acknowledged=True,
    )
    updated = service.rename_display_values(
        session.project_root,
        project_name="جديد",
        model_name="New Model",
    )
    assert updated.project_name == "جديد"
    assert session.project_root.name == f"project-{UUID(int=1).hex}"
    assert service.open_project(session.project_root).project == updated


def test_inventory_reports_managed_categories(tmp_path: Path) -> None:
    service = _service()
    session = service.create_project(
        tmp_path,
        project_name="Project",
        model_name="Model",
        locale=ProjectLocale.ENGLISH,
        mode=ProjectMode.FAST_AI,
        permission_acknowledged=True,
    )
    image = session.project_root / "inputs" / "originals" / "image.bin"
    image.write_bytes(b"1234")
    report = {item.category: item for item in service.inventory(session.project_root)}
    assert report["inputs"].file_count == 1
    assert report["inputs"].byte_size == 4
