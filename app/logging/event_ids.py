from __future__ import annotations

from enum import StrEnum


class EventId(StrEnum):
    APPLICATION_STARTED = "application.started"
    APPLICATION_STOPPED = "application.stopped"
    PROJECT_CREATED = "project.created"
    PROJECT_OPENED = "project.opened"
    PROJECT_COMMITTED = "project.committed"
    PROJECT_RECOVERY_DETECTED = "project.recovery_detected"
    PROJECT_RECOVERY_SELECTED = "project.recovery_selected"
    PROJECT_DELETE_BLOCKED = "project.delete_blocked"
    PROJECT_DELETED = "project.deleted"
    STAGE_QUEUED = "stage.queued"
    STAGE_PREFLIGHT_STARTED = "stage.preflight_started"
    STAGE_STARTED = "stage.started"
    STAGE_PROGRESS = "stage.progress"
    STAGE_PAUSE_REQUESTED = "stage.pause_requested"
    STAGE_PAUSED = "stage.paused"
    STAGE_CANCEL_REQUESTED = "stage.cancel_requested"
    STAGE_CANCELLED = "stage.cancelled"
    STAGE_SUCCEEDED = "stage.succeeded"
    STAGE_SUCCEEDED_WITH_WARNINGS = "stage.succeeded_with_warnings"
    STAGE_FAILED = "stage.failed"
    STAGE_BLOCKED = "stage.blocked"
    ENGINE_DISCOVERED = "engine.discovered"
    ENGINE_PREFLIGHT_PASSED = "engine.preflight_passed"
    ENGINE_PREFLIGHT_FAILED = "engine.preflight_failed"
    EXTERNAL_CONSENT_GRANTED = "privacy.external_consent_granted"
    EXTERNAL_CONSENT_DENIED = "privacy.external_consent_denied"
    EXPORT_STARTED = "export.started"
    EXPORT_VALIDATED = "export.validated"
    EXPORT_FAILED = "export.failed"


def event_catalog() -> tuple[str, ...]:
    return tuple(event.value for event in EventId)
