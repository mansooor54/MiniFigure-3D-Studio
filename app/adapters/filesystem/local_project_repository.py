from __future__ import annotations

import json
import os
from collections.abc import Mapping
from datetime import datetime
from pathlib import Path
from typing import Final
from uuid import UUID

from pydantic import ValidationError

from app.adapters.filesystem.atomic_file_writer import AtomicFileWriter
from app.adapters.filesystem.reparse_point_guard import assert_no_reparse_points
from app.config.paths import ProjectLayout
from app.models.project import Project
from app.ports.clock import Clock
from app.ports.project_repository import ProjectSummary, RecoveryCandidate

_MAXIMUM_MANIFEST_BYTES: Final[int] = 5 * 1024 * 1024
_MAXIMUM_JOURNAL_LINE_BYTES: Final[int] = 64 * 1024


class ProjectRepositoryError(RuntimeError):
    """Base exception for local project persistence failures."""


class ProjectCorruptError(ProjectRepositoryError):
    """Raised when committed project state cannot be validated."""


class UnsupportedProjectSchemaError(ProjectRepositoryError):
    """Raised when no migration path exists for a project schema."""


class LocalProjectRepository:
    def __init__(self, clock: Clock) -> None:
        self._clock = clock

    def create(self, project_root: Path, project: Project) -> None:
        if project_root.exists() and any(project_root.iterdir()):
            raise FileExistsError("project root is not empty")
        project_root.mkdir(parents=True, exist_ok=True)
        assert_no_reparse_points(project_root, project_root)
        layout = ProjectLayout(project_root)
        for directory in layout.managed_directories():
            directory.mkdir(parents=True, exist_ok=True)
        self._write_manifest(layout, project)
        self.append_journal_event(
            project_root,
            {
                "event_type": "project_created",
                "project_id": str(project.project_id),
                "recorded_at": self._clock.now().isoformat(),
            },
        )

    def load(self, project_root: Path) -> Project:
        layout = ProjectLayout(project_root)
        assert_no_reparse_points(project_root, layout.manifest)
        if not layout.manifest.is_file():
            raise ProjectCorruptError("project manifest is missing")
        if layout.manifest.stat().st_size > _MAXIMUM_MANIFEST_BYTES:
            raise ProjectCorruptError("project manifest exceeds the size limit")
        try:
            payload = json.loads(layout.manifest.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise ProjectCorruptError("project manifest cannot be decoded") from error
        if not isinstance(payload, dict):
            raise ProjectCorruptError("project manifest must be an object")
        schema_version = payload.get("schema_version")
        if schema_version != 1:
            raise UnsupportedProjectSchemaError(
                f"unsupported project schema version: {schema_version!r}"
            )
        try:
            return Project.model_validate(payload)
        except ValidationError as error:
            raise ProjectCorruptError("project manifest failed domain validation") from error

    def commit(self, project_root: Path, project: Project) -> None:
        current = self.load(project_root)
        if current.project_id != project.project_id:
            raise ProjectRepositoryError("project ID cannot change during commit")
        self._write_manifest(ProjectLayout(project_root), project)
        self.append_journal_event(
            project_root,
            {
                "event_type": "project_committed",
                "project_id": str(project.project_id),
                "recorded_at": self._clock.now().isoformat(),
            },
        )

    def list_projects(self, projects_root: Path) -> tuple[ProjectSummary, ...]:
        if not projects_root.exists():
            return ()
        summaries: list[ProjectSummary] = []
        for child in sorted(projects_root.iterdir(), key=lambda path: path.name.casefold()):
            if not child.is_dir() or child.is_symlink():
                continue
            try:
                project = self.load(child)
                recovery_required = bool(self.detect_recovery(child))
            except ProjectRepositoryError:
                continue
            summaries.append(
                ProjectSummary(
                    project_id=project.project_id,
                    project_name=project.project_name,
                    model_name=project.model_name,
                    project_root=child,
                    updated_at=project.updated_at,
                    recovery_required=recovery_required,
                )
            )
        return tuple(sorted(summaries, key=lambda item: item.updated_at, reverse=True))

    def detect_recovery(self, project_root: Path) -> tuple[RecoveryCandidate, ...]:
        project = self.load(project_root)
        open_runs: dict[UUID, tuple[str, str | None]] = {}
        for event in self._read_journal(ProjectLayout(project_root)):
            event_type = event.get("event_type")
            raw_run_id = event.get("run_id")
            if not isinstance(raw_run_id, str):
                continue
            try:
                run_id = UUID(raw_run_id)
            except ValueError as error:
                raise ProjectCorruptError("journal contains an invalid run ID") from error
            stage_id = event.get("stage_id")
            if not isinstance(stage_id, str):
                raise ProjectCorruptError("run journal event is missing stage_id")
            if event_type == "run_started":
                open_runs[run_id] = (stage_id, None)
            elif event_type == "checkpoint_committed" and run_id in open_runs:
                checkpoint = event.get("checkpoint_relative_path")
                if checkpoint is not None and not isinstance(checkpoint, str):
                    raise ProjectCorruptError("checkpoint path must be a string")
                open_runs[run_id] = (stage_id, checkpoint)
            elif event_type == "run_terminal":
                open_runs.pop(run_id, None)
        detected_at = self._clock.now()
        return tuple(
            RecoveryCandidate(
                project_id=project.project_id,
                project_root=project_root,
                run_id=run_id,
                stage_id=stage_id,
                checkpoint_relative_path=checkpoint,
                detected_at=detected_at,
            )
            for run_id, (stage_id, checkpoint) in sorted(
                open_runs.items(), key=lambda item: item[0].hex
            )
        )

    def append_journal_event(self, project_root: Path, event: Mapping[str, object]) -> None:
        layout = ProjectLayout(project_root)
        assert_no_reparse_points(project_root, layout.journal)
        encoded = (json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
        if len(encoded) > _MAXIMUM_JOURNAL_LINE_BYTES:
            raise ProjectRepositoryError("journal event exceeds the size limit")
        with layout.journal.open("ab") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())

    @staticmethod
    def _write_manifest(layout: ProjectLayout, project: Project) -> None:
        writer = AtomicFileWriter(layout.root)

        def validate(path: Path) -> None:
            payload = json.loads(path.read_text(encoding="utf-8"))
            Project.model_validate(payload)

        writer.write_json(
            layout.manifest,
            project.model_dump(mode="json"),
            validate=validate,
        )

    @staticmethod
    def _read_journal(layout: ProjectLayout) -> tuple[dict[str, object], ...]:
        if not layout.journal.exists():
            return ()
        if layout.journal.is_symlink():
            raise ProjectCorruptError("project journal cannot be a symbolic link")
        events: list[dict[str, object]] = []
        try:
            with layout.journal.open("rb") as handle:
                for line in handle:
                    if len(line) > _MAXIMUM_JOURNAL_LINE_BYTES:
                        raise ProjectCorruptError("journal line exceeds the size limit")
                    payload = json.loads(line.decode("utf-8"))
                    if not isinstance(payload, dict):
                        raise ProjectCorruptError("journal event must be an object")
                    events.append(payload)
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise ProjectCorruptError("project journal cannot be decoded") from error
        return tuple(events)


def parse_journal_timestamp(event: Mapping[str, object]) -> datetime:
    raw = event.get("recorded_at")
    if not isinstance(raw, str):
        raise ProjectCorruptError("journal event is missing recorded_at")
    try:
        value = datetime.fromisoformat(raw)
    except ValueError as error:
        raise ProjectCorruptError("journal timestamp is invalid") from error
    if value.tzinfo is None or value.utcoffset() is None:
        raise ProjectCorruptError("journal timestamp must include a timezone")
    return value
