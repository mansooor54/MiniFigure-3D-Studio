from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Final
from uuid import UUID

from jsonschema import Draft202012Validator, FormatChecker

from app.models.stage_result import StageResult, StageStatus

_ROOT: Final[Path] = Path(__file__).resolve().parents[2]
_SCHEMA_ROOT: Final[Path] = _ROOT / "app" / "config" / "schemas"


def _schema(filename: str) -> dict[str, object]:
    data = json.loads((_SCHEMA_ROOT / filename).read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def _request_payload() -> dict[str, object]:
    return {
        "protocol_version": 1,
        "request_id": str(UUID(int=1)),
        "run_id": str(UUID(int=2)),
        "stage_id": "shape_generation",
        "inputs": [
            {
                "artifact_id": str(UUID(int=3)),
                "role": "prepared_image",
                "relative_path": "inputs/prepared/image.png",
                "sha256": "2" * 64,
            }
        ],
        "expected_outputs": [
            {"role": "raw_mesh", "relative_path": "artifacts/raw/model.glb"}
        ],
        "parameters": {"height_mm": 100.0},
        "cancellation_token_relative_path": "runs/0001/cancel.token",
        "redaction_policy_version": 1,
    }


def test_worker_schemas_are_valid_draft_2020_12() -> None:
    Draft202012Validator.check_schema(_schema("worker_request.schema.json"))
    Draft202012Validator.check_schema(_schema("worker_result.schema.json"))


def test_worker_request_validates() -> None:
    validator = Draft202012Validator(
        _schema("worker_request.schema.json"),
        format_checker=FormatChecker(),
    )
    validator.validate(_request_payload())


def test_worker_request_rejects_path_escape() -> None:
    payload = _request_payload()
    payload["cancellation_token_relative_path"] = "../cancel.token"
    validator = Draft202012Validator(
        _schema("worker_request.schema.json"),
        format_checker=FormatChecker(),
    )
    assert list(validator.iter_errors(payload))


def test_stage_result_validates_against_worker_result_schema() -> None:
    timestamp = datetime(2026, 1, 1, tzinfo=UTC)
    result = StageResult(
        run_id=UUID(int=2),
        stage_id="shape_generation",
        status=StageStatus.SUCCEEDED,
        started_at=timestamp,
        finished_at=timestamp,
    )
    validator = Draft202012Validator(
        _schema("worker_result.schema.json"),
        format_checker=FormatChecker(),
    )
    validator.validate(result.model_dump(mode="json"))


def test_worker_request_rejects_unknown_top_level_property() -> None:
    payload = _request_payload()
    payload["provider_secret"] = "forbidden"
    validator = Draft202012Validator(_schema("worker_request.schema.json"))
    errors = list(validator.iter_errors(payload))
    assert any("Additional properties are not allowed" in error.message for error in errors)
