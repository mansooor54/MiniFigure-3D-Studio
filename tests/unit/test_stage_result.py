from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID

import pytest
from pydantic import ValidationError

from app.models.error_info import ErrorCategory, ErrorInfo
from app.models.stage_result import ArtifactReference, StageResult, StageStatus

_NOW = datetime(2026, 1, 1, tzinfo=UTC)
_HASH = "a" * 64


def _artifact() -> ArtifactReference:
    return ArtifactReference(
        artifact_id=UUID(int=3),
        role="raw_mesh",
        relative_path="artifacts/raw/model.glb",
        sha256=_HASH,
    )


def _error() -> ErrorInfo:
    return ErrorInfo(
        code="AI_GENERATION_FAILED",
        category=ErrorCategory.ENGINE,
        user_message_key="error.ai.generation_failed",
        technical_summary="The worker returned a structured failure.",
        retryable=True,
    )


def test_success_result_accepts_verified_artifact_reference() -> None:
    result = StageResult(
        run_id=UUID(int=1),
        stage_id="shape_generation",
        status=StageStatus.SUCCEEDED,
        started_at=_NOW,
        finished_at=_NOW + timedelta(seconds=1),
        artifacts=(_artifact(),),
    )
    assert result.status is StageStatus.SUCCEEDED
    assert result.artifacts[0].relative_path.endswith("model.glb")


def test_warning_result_requires_warning_code() -> None:
    with pytest.raises(ValidationError, match="requires warning codes"):
        StageResult(
            run_id=UUID(int=1),
            stage_id="shape_generation",
            status=StageStatus.SUCCEEDED_WITH_WARNINGS,
            started_at=_NOW,
            finished_at=_NOW,
        )


def test_failed_result_requires_structured_error() -> None:
    with pytest.raises(ValidationError, match="require an error"):
        StageResult(
            run_id=UUID(int=1),
            stage_id="shape_generation",
            status=StageStatus.FAILED,
            started_at=_NOW,
            finished_at=_NOW,
        )


def test_cancelled_result_cannot_promote_artifacts() -> None:
    with pytest.raises(ValidationError, match="cannot promote artifacts"):
        StageResult(
            run_id=UUID(int=1),
            stage_id="shape_generation",
            status=StageStatus.CANCELLED,
            started_at=_NOW,
            finished_at=_NOW,
            artifacts=(_artifact(),),
            error=_error(),
        )


def test_finish_time_cannot_precede_start_time() -> None:
    with pytest.raises(ValidationError, match="must not precede"):
        StageResult(
            run_id=UUID(int=1),
            stage_id="shape_generation",
            status=StageStatus.FAILED,
            started_at=_NOW,
            finished_at=_NOW - timedelta(seconds=1),
            error=_error(),
        )
