from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Protocol
from uuid import UUID

from app.adapters.filesystem.artifact_hasher import ArtifactHasher
from app.adapters.filesystem.atomic_file_writer import AtomicFileWriter
from app.adapters.filesystem.safe_paths import project_relative_path, resolve_project_child
from app.ports.clock import Clock


class JournalWriter(Protocol):
    def append_journal_event(self, project_root: Path, event: Mapping[str, object]) -> None:
        """Append and durably flush one structured journal event."""


@dataclass(frozen=True)
class CheckpointRecord:
    checkpoint_id: UUID
    project_id: UUID
    run_id: UUID
    stage_id: str
    created_at: datetime
    relative_path: str
    sha256: str
    byte_size: int


class CheckpointManager:
    def __init__(
        self,
        project_root: Path,
        journal: JournalWriter,
        clock: Clock,
    ) -> None:
        self._project_root = project_root.resolve(strict=False)
        self._journal = journal
        self._clock = clock
        self._writer = AtomicFileWriter(self._project_root)
        self._hasher = ArtifactHasher(self._project_root)

    def register(
        self,
        *,
        checkpoint_id: UUID,
        project_id: UUID,
        run_id: UUID,
        stage_id: str,
        state: Mapping[str, object],
    ) -> CheckpointRecord:
        relative = f"runs/{run_id.hex}/checkpoints/{checkpoint_id.hex}.json"
        target = resolve_project_child(self._project_root, relative)
        created_at = self._clock.now()
        envelope = {
            "checkpoint_id": str(checkpoint_id),
            "project_id": str(project_id),
            "run_id": str(run_id),
            "stage_id": stage_id,
            "created_at": created_at.isoformat(),
            "state": dict(state),
        }

        def validate(path: Path) -> None:
            loaded = json.loads(path.read_text(encoding="utf-8"))
            if loaded != envelope:
                raise ValueError("checkpoint round-trip mismatch")

        self._writer.write_json(target, envelope, validate=validate)
        hashed = self._hasher.hash_file(target)
        record = CheckpointRecord(
            checkpoint_id=checkpoint_id,
            project_id=project_id,
            run_id=run_id,
            stage_id=stage_id,
            created_at=created_at,
            relative_path=project_relative_path(self._project_root, target),
            sha256=hashed.sha256,
            byte_size=hashed.byte_size,
        )
        try:
            self._journal.append_journal_event(
                self._project_root,
                {
                    "event_type": "checkpoint_committed",
                    "project_id": str(project_id),
                    "run_id": str(run_id),
                    "stage_id": stage_id,
                    "checkpoint_relative_path": record.relative_path,
                    "checkpoint_sha256": record.sha256,
                    "recorded_at": created_at.isoformat(),
                },
            )
        except Exception:
            target.unlink(missing_ok=True)
            raise
        return record

    def load_and_validate(self, record: CheckpointRecord) -> dict[str, object]:
        target = resolve_project_child(self._project_root, record.relative_path)
        hashed = self._hasher.hash_file(target, maximum_bytes=record.byte_size)
        if hashed.sha256 != record.sha256 or hashed.byte_size != record.byte_size:
            raise ValueError("checkpoint hash or size mismatch")
        payload = json.loads(target.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("checkpoint must be a JSON object")
        expected = {
            "checkpoint_id": str(record.checkpoint_id),
            "project_id": str(record.project_id),
            "run_id": str(record.run_id),
            "stage_id": record.stage_id,
            "created_at": record.created_at.isoformat(),
        }
        if any(payload.get(key) != value for key, value in expected.items()):
            raise ValueError("checkpoint identity mismatch")
        state = payload.get("state")
        if not isinstance(state, dict):
            raise ValueError("checkpoint state must be an object")
        return state

    @staticmethod
    def as_journal_safe_dict(record: CheckpointRecord) -> dict[str, object]:
        values = asdict(record)
        values["checkpoint_id"] = str(record.checkpoint_id)
        values["project_id"] = str(record.project_id)
        values["run_id"] = str(record.run_id)
        values["created_at"] = record.created_at.isoformat()
        return values
