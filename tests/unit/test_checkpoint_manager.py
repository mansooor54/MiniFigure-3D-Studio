from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

import pytest

from app.workers.checkpoint_manager import CheckpointManager


@dataclass(frozen=True)
class FixedClock:
    value: datetime

    def now(self) -> datetime:
        return self.value


@dataclass
class RecordingJournal:
    events: list[dict[str, object]] = field(default_factory=list)
    fail: bool = False

    def append_journal_event(self, _project_root: Path, event: Mapping[str, object]) -> None:
        if self.fail:
            raise OSError("seeded journal failure")
        self.events.append(dict(event))


def test_checkpoint_registers_journal_and_round_trips_state(tmp_path: Path) -> None:
    journal = RecordingJournal()
    manager = CheckpointManager(
        tmp_path,
        journal,
        FixedClock(datetime(2026, 1, 1, tzinfo=UTC)),
    )
    record = manager.register(
        checkpoint_id=UUID(int=1),
        project_id=UUID(int=2),
        run_id=UUID(int=3),
        stage_id="shape_generation",
        state={"completed_units": 4, "engine_state": "ready"},
    )
    assert manager.load_and_validate(record) == {
        "completed_units": 4,
        "engine_state": "ready",
    }
    assert journal.events[0]["checkpoint_sha256"] == record.sha256


def test_checkpoint_tamper_is_rejected(tmp_path: Path) -> None:
    manager = CheckpointManager(
        tmp_path,
        RecordingJournal(),
        FixedClock(datetime(2026, 1, 1, tzinfo=UTC)),
    )
    record = manager.register(
        checkpoint_id=UUID(int=1),
        project_id=UUID(int=2),
        run_id=UUID(int=3),
        stage_id="shape_generation",
        state={"completed_units": 4},
    )
    (tmp_path / record.relative_path).write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="hash or size mismatch"):
        manager.load_and_validate(record)


def test_journal_failure_removes_unregistered_checkpoint(tmp_path: Path) -> None:
    manager = CheckpointManager(
        tmp_path,
        RecordingJournal(fail=True),
        FixedClock(datetime(2026, 1, 1, tzinfo=UTC)),
    )
    with pytest.raises(OSError, match="seeded journal failure"):
        manager.register(
            checkpoint_id=UUID(int=1),
            project_id=UUID(int=2),
            run_id=UUID(int=3),
            stage_id="shape_generation",
            state={"completed_units": 4},
        )
    assert list(tmp_path.rglob("*.json")) == []
