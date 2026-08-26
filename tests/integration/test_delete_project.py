from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

import pytest

from app.adapters.filesystem.local_project_repository import LocalProjectRepository
from app.models.project import Project, ProjectLocale, ProjectMode
from app.services.secure_deletion_service import DeletionStatus, SecureDeletionService


@dataclass(frozen=True)
class FixedClock:
    value: datetime

    def now(self) -> datetime:
        return self.value


def _setup(tmp_path: Path) -> tuple[Path, SecureDeletionService]:
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
    service = SecureDeletionService(
        repository,
        clock,
        uuid_factory=lambda: UUID(int=2),
    )
    return root, service


def _receipt_payload(tmp_path: Path) -> dict[str, object]:
    receipt_files = list((tmp_path / ".deletion-receipts").glob("*.json"))
    assert len(receipt_files) == 1
    payload = json.loads(receipt_files[0].read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_active_project_deletion_is_blocked_without_removing_data(tmp_path: Path) -> None:
    root, service = _setup(tmp_path)
    receipt = service.delete_project(
        root,
        expected_project_id=UUID(int=1),
        active_job_count=1,
        project_is_open=False,
    )
    assert receipt.status is DeletionStatus.BLOCKED
    assert root.is_dir()
    assert "no active jobs" in (receipt.reason or "")
    assert _receipt_payload(tmp_path)["status"] == "blocked"


def test_closed_project_is_logically_deleted_with_truthful_receipt(tmp_path: Path) -> None:
    root, service = _setup(tmp_path)
    artifact = root / "artifacts" / "processed" / "model.glb"
    artifact.write_bytes(b"12345")
    artifact.chmod(0o444)
    receipt = service.delete_project(
        root,
        expected_project_id=UUID(int=1),
        active_job_count=0,
        project_is_open=False,
    )
    assert receipt.status is DeletionStatus.DELETED
    assert not root.exists()
    assert receipt.deleted_file_count >= 3
    assert receipt.deleted_byte_size >= 5
    assert "snapshots" in receipt.storage_notice
    payload = _receipt_payload(tmp_path)
    assert payload["status"] == "deleted"
    assert "secure overwrite" not in str(payload).lower()


def test_project_identity_mismatch_is_blocked(tmp_path: Path) -> None:
    root, service = _setup(tmp_path)
    receipt = service.delete_project(
        root,
        expected_project_id=UUID(int=99),
        active_job_count=0,
        project_is_open=False,
    )
    assert receipt.status is DeletionStatus.BLOCKED
    assert root.exists()


def test_symlink_in_project_blocks_deletion_and_preserves_external_target(
    tmp_path: Path,
) -> None:
    root, service = _setup(tmp_path)
    outside = tmp_path / "outside.txt"
    outside.write_text("preserve", encoding="utf-8")
    link = root / "inputs" / "originals" / "outside-link.txt"
    try:
        link.symlink_to(outside)
    except OSError as error:
        pytest.skip(f"symlink creation is unavailable: {error}")
    receipt = service.delete_project(
        root,
        expected_project_id=UUID(int=1),
        active_job_count=0,
        project_is_open=False,
    )
    assert receipt.status is DeletionStatus.BLOCKED
    assert root.exists()
    assert outside.read_text(encoding="utf-8") == "preserve"
