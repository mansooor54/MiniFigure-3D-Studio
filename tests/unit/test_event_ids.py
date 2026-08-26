from __future__ import annotations

import re

from app.logging.event_ids import EventId, event_catalog


def test_event_catalog_is_unique_and_stable() -> None:
    catalog = event_catalog()
    assert len(catalog) == len(set(catalog))
    assert all(re.fullmatch(r"[a-z][a-z0-9_.]+", event_id) for event_id in catalog)


def test_event_catalog_covers_critical_outcomes() -> None:
    required = {
        EventId.PROJECT_CREATED,
        EventId.PROJECT_RECOVERY_DETECTED,
        EventId.PROJECT_DELETE_BLOCKED,
        EventId.PROJECT_DELETED,
        EventId.STAGE_SUCCEEDED,
        EventId.STAGE_FAILED,
        EventId.STAGE_BLOCKED,
        EventId.ENGINE_PREFLIGHT_FAILED,
        EventId.EXTERNAL_CONSENT_GRANTED,
        EventId.EXPORT_VALIDATED,
        EventId.EXPORT_FAILED,
    }
    assert required.issubset(set(EventId))
