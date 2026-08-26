from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID

import pytest
from pydantic import ValidationError

from app.models.pipeline_run import (
    EngineReference,
    PipelineRun,
    PipelineState,
    StageRecord,
    StageState,
)

_NOW = datetime(2026, 1, 1, tzinfo=UTC)
_HASH = "b" * 64


def _stage(stage_id: str = "image_import") -> StageRecord:
    return StageRecord(
        stage_id=stage_id,
        state=StageState.SUCCEEDED,
        started_at=_NOW,
        finished_at=_NOW + timedelta(seconds=1),
        output_artifact_ids=(UUID(int=4),),
        result_relative_path=f"runs/00000000/{stage_id}/result.json",
    )


def test_pipeline_run_preserves_engine_and_stage_provenance() -> None:
    run = PipelineRun(
        run_id=UUID(int=1),
        project_id=UUID(int=2),
        state=PipelineState.RUNNING,
        settings_sha256=_HASH,
        created_at=_NOW,
        updated_at=_NOW + timedelta(seconds=2),
        engines=(
            EngineReference(
                engine_id="fake.generator",
                version="1.0.0",
                manifest_sha256=_HASH,
                device_summary="synthetic test device",
            ),
        ),
        stages=(_stage(),),
    )
    assert run.engines[0].engine_id == "fake.generator"
    assert run.stages[0].output_artifact_ids == (UUID(int=4),)


def test_pipeline_run_rejects_duplicate_stage_ids() -> None:
    with pytest.raises(ValidationError, match="stage_id values must be unique"):
        PipelineRun(
            run_id=UUID(int=1),
            project_id=UUID(int=2),
            state=PipelineState.RUNNING,
            settings_sha256=_HASH,
            created_at=_NOW,
            updated_at=_NOW,
            stages=(_stage(), _stage()),
        )


def test_stage_finish_requires_start() -> None:
    with pytest.raises(ValidationError, match="requires started_at"):
        StageRecord(
            stage_id="image_import",
            state=StageState.FAILED,
            finished_at=_NOW,
        )


def test_pipeline_update_cannot_precede_creation() -> None:
    with pytest.raises(ValidationError, match="must not precede"):
        PipelineRun(
            run_id=UUID(int=1),
            project_id=UUID(int=2),
            state=PipelineState.DRAFT,
            settings_sha256=_HASH,
            created_at=_NOW,
            updated_at=_NOW - timedelta(seconds=1),
        )
