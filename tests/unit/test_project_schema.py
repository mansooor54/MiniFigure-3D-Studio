from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Final
from uuid import UUID

from jsonschema import Draft202012Validator, FormatChecker

from app.models.project import Project, ProjectLocale, ProjectMode
from scripts.generate_json_schemas import generate

_ROOT: Final[Path] = Path(__file__).resolve().parents[2]
_SCHEMA_PATH: Final[Path] = _ROOT / "app" / "config" / "schemas" / "project.schema.json"


def _schema() -> dict[str, object]:
    data = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def _project_payload() -> dict[str, object]:
    timestamp = datetime(2026, 1, 1, tzinfo=UTC)
    project = Project(
        project_id=UUID(int=1),
        project_name="مشروع",
        model_name="Mini Noor",
        locale=ProjectLocale.ARABIC,
        mode=ProjectMode.FAST_AI,
        created_at=timestamp,
        updated_at=timestamp,
        subject_permission_acknowledged_at=timestamp,
    )
    return project.model_dump(mode="json")


def test_project_schema_is_valid_draft_2020_12() -> None:
    Draft202012Validator.check_schema(_schema())


def test_project_model_serialization_validates_against_schema() -> None:
    validator = Draft202012Validator(_schema(), format_checker=FormatChecker())
    validator.validate(_project_payload())


def test_project_schema_rejects_unknown_property() -> None:
    payload = _project_payload()
    payload["unexpected"] = True
    validator = Draft202012Validator(_schema(), format_checker=FormatChecker())
    errors = list(validator.iter_errors(payload))
    assert any("Additional properties are not allowed" in error.message for error in errors)


def test_committed_schemas_match_deterministic_generator(tmp_path: Path) -> None:
    output_root = tmp_path / "schemas"
    generate(output_root)
    committed_root = _SCHEMA_PATH.parent
    for generated in sorted(output_root.glob("*.json")):
        committed = committed_root / generated.name
        assert generated.read_bytes() == committed.read_bytes()
