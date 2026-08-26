from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from uuid import UUID, uuid4

from app.adapters.filesystem.atomic_file_writer import AtomicFileWriter
from app.adapters.filesystem.reparse_point_guard import (
    ReparsePointError,
    assert_no_reparse_points,
    is_reparse_point,
)
from app.ports.clock import Clock
from app.ports.project_repository import ProjectRepository

UuidFactory = Callable[[], UUID]


class DeletionStatus(StrEnum):
    DELETED = "deleted"
    PARTIAL = "partial"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class DeletionReceipt:
    request_id: UUID
    project_id: UUID
    project_directory_name: str
    status: DeletionStatus
    started_at: datetime
    completed_at: datetime
    deleted_file_count: int
    deleted_byte_size: int
    remaining_relative_paths: tuple[str, ...]
    reason: str | None
    storage_notice: str = (
        "Logical application deletion only; storage snapshots, backups, and flash-memory "
        "remapping may retain recoverable copies."
    )


class SecureDeletionService:
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

    def delete_project(
        self,
        project_root: Path,
        *,
        expected_project_id: UUID,
        active_job_count: int,
        project_is_open: bool,
    ) -> DeletionReceipt:
        started_at = self._clock.now()
        request_id = self._uuid_factory()
        project = self._repository.load(project_root)
        if project.project_id != expected_project_id:
            return self._blocked_receipt(
                project_root,
                request_id,
                project.project_id,
                started_at,
                "project identity does not match the deletion request",
            )
        if active_job_count != 0 or project_is_open:
            return self._blocked_receipt(
                project_root,
                request_id,
                project.project_id,
                started_at,
                "project must be closed and have no active jobs",
            )
        try:
            file_count, byte_size = self._preflight(project_root)
        except (OSError, ReparsePointError) as error:
            return self._blocked_receipt(
                project_root,
                request_id,
                project.project_id,
                started_at,
                str(error),
            )
        quarantine = project_root.with_name(
            f".deleting-{project.project_id.hex}-{request_id.hex}"
        )
        if quarantine.exists():
            return self._blocked_receipt(
                project_root,
                request_id,
                project.project_id,
                started_at,
                "deletion quarantine path already exists",
            )
        os.replace(project_root, quarantine)
        remaining = self._remove_tree_without_following(quarantine)
        status = DeletionStatus.DELETED if not remaining else DeletionStatus.PARTIAL
        receipt = DeletionReceipt(
            request_id=request_id,
            project_id=project.project_id,
            project_directory_name=project_root.name,
            status=status,
            started_at=started_at,
            completed_at=self._clock.now(),
            deleted_file_count=file_count - self._remaining_file_count(quarantine),
            deleted_byte_size=byte_size - self._remaining_byte_size(quarantine),
            remaining_relative_paths=remaining,
            reason=None if status is DeletionStatus.DELETED else "some items could not be removed",
        )
        self._write_receipt(project_root.parent, receipt)
        return receipt

    def _blocked_receipt(
        self,
        project_root: Path,
        request_id: UUID,
        project_id: UUID,
        started_at: datetime,
        reason: str,
    ) -> DeletionReceipt:
        receipt = DeletionReceipt(
            request_id=request_id,
            project_id=project_id,
            project_directory_name=project_root.name,
            status=DeletionStatus.BLOCKED,
            started_at=started_at,
            completed_at=self._clock.now(),
            deleted_file_count=0,
            deleted_byte_size=0,
            remaining_relative_paths=(),
            reason=reason,
        )
        self._write_receipt(project_root.parent, receipt)
        return receipt

    @staticmethod
    def _preflight(project_root: Path) -> tuple[int, int]:
        assert_no_reparse_points(project_root, project_root)
        file_count = 0
        byte_size = 0
        for current, directories, files in os.walk(project_root, followlinks=False):
            current_path = Path(current)
            for name in (*directories, *files):
                candidate = current_path / name
                if is_reparse_point(candidate):
                    raise ReparsePointError(
                        f"project contains a reparse point and was not deleted: {name}"
                    )
            for name in files:
                candidate = current_path / name
                file_count += 1
                byte_size += candidate.stat().st_size
        return file_count, byte_size

    @staticmethod
    def _remove_tree_without_following(root: Path) -> tuple[str, ...]:
        failures: list[str] = []
        for current, directories, files in os.walk(root, topdown=False, followlinks=False):
            current_path = Path(current)
            for name in files:
                candidate = current_path / name
                try:
                    candidate.chmod(0o600)
                    candidate.unlink()
                except OSError:
                    failures.append(candidate.relative_to(root).as_posix())
            for name in directories:
                candidate = current_path / name
                try:
                    candidate.rmdir()
                except OSError:
                    failures.append(candidate.relative_to(root).as_posix())
        try:
            root.rmdir()
        except OSError:
            failures.append(".")
        return tuple(sorted(set(failures)))

    @staticmethod
    def _remaining_file_count(root: Path) -> int:
        return sum(1 for path in root.rglob("*") if path.is_file()) if root.exists() else 0

    @staticmethod
    def _remaining_byte_size(root: Path) -> int:
        return (
            sum(path.stat().st_size for path in root.rglob("*") if path.is_file())
            if root.exists()
            else 0
        )

    @staticmethod
    def _write_receipt(parent: Path, receipt: DeletionReceipt) -> None:
        receipt_root = parent / ".deletion-receipts"
        receipt_path = receipt_root / f"{receipt.project_id.hex}-{receipt.request_id.hex}.json"
        payload = asdict(receipt)
        payload["request_id"] = str(receipt.request_id)
        payload["project_id"] = str(receipt.project_id)
        payload["status"] = receipt.status.value
        payload["started_at"] = receipt.started_at.isoformat()
        payload["completed_at"] = receipt.completed_at.isoformat()
        AtomicFileWriter(parent).write_json(receipt_path, payload)
