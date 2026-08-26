from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Final
from uuid import UUID

from jsonschema import Draft202012Validator, FormatChecker

_ROOT: Final[Path] = Path(__file__).resolve().parents[2]
_SCHEMA_PATH: Final[Path] = (
    _ROOT / "app" / "config" / "schemas" / "validation_report.schema.json"
)


def _schema() -> dict[str, object]:
    data = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def _payload() -> dict[str, object]:
    return {
        "schema_version": 1,
        "report_id": str(UUID(int=1)),
        "artifact_id": str(UUID(int=2)),
        "created_at": datetime(2026, 1, 1, tzinfo=UTC).isoformat(),
        "validator_versions": {"topology": "1.0.0"},
        "metrics": {"non_manifold_edges": 0, "height_mm": 100.0},
        "findings": [],
        "status": "ready_to_print",
        "export_blocked": False,
        "recommended_orientation": "base_down_z_positive",
        "support_requirement": "low",
    }


def test_validation_report_schema_is_valid_draft_2020_12() -> None:
    Draft202012Validator.check_schema(_schema())


def test_ready_to_print_report_validates() -> None:
    Draft202012Validator(_schema(), format_checker=FormatChecker()).validate(_payload())


def test_repair_required_blocking_finding_validates() -> None:
    payload = _payload()
    payload["status"] = "repair_required"
    payload["export_blocked"] = True
    payload["findings"] = [
        {
            "code": "NON_MANIFOLD_BLOCKER",
            "severity": "error",
            "message_key": "validation.non_manifold.blocker",
            "blocking": True,
            "automatic_repair_available": True,
            "measured_value": 12,
            "threshold": 0,
            "geometry_reference": "mesh.main",
        }
    ]
    Draft202012Validator(_schema(), format_checker=FormatChecker()).validate(payload)


def test_validation_report_rejects_unknown_status() -> None:
    payload = _payload()
    payload["status"] = "perfect"
    assert list(Draft202012Validator(_schema()).iter_errors(payload))


def test_validation_report_rejects_unknown_property() -> None:
    payload = _payload()
    payload["guaranteed_print_success"] = True
    errors = list(Draft202012Validator(_schema()).iter_errors(payload))
    assert any("Additional properties are not allowed" in error.message for error in errors)
