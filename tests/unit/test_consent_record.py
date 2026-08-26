from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID

import pytest
from pydantic import ValidationError

from app.models.consent_record import (
    ConsentDecision,
    ConsentRecord,
    ConsentScope,
    DataCategory,
)

_NOW = datetime(2026, 1, 1, tzinfo=UTC)
_HASH = "f" * 64


def _record(**updates: object) -> ConsentRecord:
    values: dict[str, object] = {
        "consent_id": UUID(int=1),
        "project_id": UUID(int=2),
        "purpose": "external_shape_generation",
        "provider_id": "example.provider",
        "adapter_version": "1.0.0",
        "data_categories": (
            DataCategory.EXIF_STRIPPED_IMAGE,
            DataCategory.GENERATION_PARAMETERS,
        ),
        "endpoint_region": "UAE",
        "policy_url": "https://example.invalid/privacy",
        "policy_version": "2026-01",
        "decision": ConsentDecision.GRANTED,
        "scope": ConsentScope.SINGLE_OPERATION,
        "operation_id": UUID(int=3),
        "recorded_at": _NOW,
    }
    values.update(updates)
    return ConsentRecord.model_validate(values)


def test_single_operation_consent_records_exact_transfer_scope() -> None:
    record = _record()
    assert record.operation_id == UUID(int=3)
    assert DataCategory.EXIF_STRIPPED_IMAGE in record.data_categories


def test_single_operation_scope_requires_operation_id() -> None:
    with pytest.raises(ValidationError, match="requires only operation_id"):
        _record(operation_id=None)


def test_remembered_scope_requires_hash_not_operation_id() -> None:
    record = _record(
        scope=ConsentScope.BOUNDED_REMEMBERED,
        operation_id=None,
        remembered_scope_sha256=_HASH,
        expires_at=_NOW + timedelta(days=30),
    )
    assert record.remembered_scope_sha256 == _HASH


def test_duplicate_data_categories_are_rejected() -> None:
    with pytest.raises(ValidationError, match="must be unique"):
        _record(
            data_categories=(DataCategory.SOURCE_IMAGE, DataCategory.SOURCE_IMAGE),
        )


def test_expiry_must_follow_recording() -> None:
    with pytest.raises(ValidationError, match="must follow recorded_at"):
        _record(expires_at=_NOW)
