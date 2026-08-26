from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from app.adapters.filesystem.safe_paths import resolve_project_child
from app.ports.clock import Clock
from app.ports.project_repository import ProjectRepository, RecoveryCandidate
from app.workers.checkpoint_manager import JournalWriter


class RecoveryAction(StrEnum):
    RESUME_FROM_CHECKPOINT = "resume_from_checkpoint"
    RESTART_STAGE = "restart_stage"
    DISCARD_STAGED_OUTPUTS = "discard_staged_outputs"
    MARK_RUN_FAILED = "mark_run_failed"


@dataclass(frozen=True)
class RecoveryPlan:
    candidate: RecoveryCandidate
    allowed_actions: tuple[RecoveryAction, ...]
    checkpoint_valid: bool


class RecoveryCoordinator:
    def __init__(
        self,
        repository: ProjectRepository,
        journal: JournalWriter,
        clock: Clock,
    ) -> None:
        self._repository = repository
        self._journal = journal
        self._clock = clock

    def inspect(self, project_root: Path) -> tuple[RecoveryPlan, ...]:
        plans: list[RecoveryPlan] = []
        for candidate in self._repository.detect_recovery(project_root):
            checkpoint_valid = self._checkpoint_is_valid(candidate)
            actions = [
                RecoveryAction.RESTART_STAGE,
                RecoveryAction.DISCARD_STAGED_OUTPUTS,
                RecoveryAction.MARK_RUN_FAILED,
            ]
            if checkpoint_valid:
                actions.insert(0, RecoveryAction.RESUME_FROM_CHECKPOINT)
            plans.append(
                RecoveryPlan(
                    candidate=candidate,
                    allowed_actions=tuple(actions),
                    checkpoint_valid=checkpoint_valid,
                )
            )
        return tuple(plans)

    def select(self, plan: RecoveryPlan, action: RecoveryAction) -> None:
        if action not in plan.allowed_actions:
            raise ValueError("recovery action is not valid for this run")
        candidate = plan.candidate
        self._journal.append_journal_event(
            candidate.project_root,
            {
                "event_type": "recovery_selected",
                "project_id": str(candidate.project_id),
                "run_id": str(candidate.run_id),
                "stage_id": candidate.stage_id,
                "action": action.value,
                "recorded_at": self._clock.now().isoformat(),
            },
        )
        if action is RecoveryAction.MARK_RUN_FAILED:
            self.mark_terminal(plan, terminal_status="failed_during_recovery")

    def mark_terminal(self, plan: RecoveryPlan, *, terminal_status: str) -> None:
        candidate = plan.candidate
        self._journal.append_journal_event(
            candidate.project_root,
            {
                "event_type": "run_terminal",
                "project_id": str(candidate.project_id),
                "run_id": str(candidate.run_id),
                "stage_id": candidate.stage_id,
                "terminal_status": terminal_status,
                "recorded_at": self._clock.now().isoformat(),
            },
        )

    @staticmethod
    def _checkpoint_is_valid(candidate: RecoveryCandidate) -> bool:
        if candidate.checkpoint_relative_path is None:
            return False
        try:
            checkpoint = resolve_project_child(
                candidate.project_root,
                candidate.checkpoint_relative_path,
            )
            payload = json.loads(checkpoint.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError):
            return False
        if not isinstance(payload, dict):
            return False
        return (
            payload.get("project_id") == str(candidate.project_id)
            and payload.get("run_id") == str(candidate.run_id)
            and payload.get("stage_id") == candidate.stage_id
            and isinstance(payload.get("state"), dict)
        )
