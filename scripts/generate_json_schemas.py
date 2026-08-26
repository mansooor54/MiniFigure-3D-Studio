from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Final

from app.application_info import (
    VALIDATION_REPORT_SCHEMA_VERSION,
    WORKER_PROTOCOL_VERSION,
)
from app.models.engine_manifest import EngineManifest
from app.models.project import Project
from app.models.stage_result import StageResult

_SCHEMA_URI: Final[str] = "https://json-schema.org/draft/2020-12/schema"
_IDENTIFIER_PATTERN: Final[str] = "^[a-z][a-z0-9._-]{1,127}$"
_RELATIVE_PATH_PATTERN: Final[str] = r"^(?!/)(?!.*(?:^|/)\.\.(?:/|$))(?!.*\\).+$"
_SHA256_PATTERN: Final[str] = "^[0-9a-f]{64}$"


def _pydantic_schema(
    model: type[Project] | type[EngineManifest] | type[StageResult],
) -> dict[str, Any]:
    schema = model.model_json_schema(mode="validation")
    schema["$schema"] = _SCHEMA_URI
    return schema


def _artifact_reference_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["artifact_id", "role", "relative_path", "sha256"],
        "properties": {
            "artifact_id": {"type": "string", "format": "uuid"},
            "role": {"type": "string", "pattern": _IDENTIFIER_PATTERN},
            "relative_path": {"type": "string", "pattern": _RELATIVE_PATH_PATTERN},
            "sha256": {"type": "string", "pattern": _SHA256_PATTERN},
        },
    }


def _worker_request_schema() -> dict[str, Any]:
    return {
        "$schema": _SCHEMA_URI,
        "$id": "https://minifigure3dstudio.local/schemas/worker-request-v1.json",
        "title": "MiniFigure Worker Request",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "protocol_version",
            "request_id",
            "run_id",
            "stage_id",
            "inputs",
            "expected_outputs",
            "parameters",
            "cancellation_token_relative_path",
            "redaction_policy_version",
        ],
        "properties": {
            "protocol_version": {"const": WORKER_PROTOCOL_VERSION},
            "request_id": {"type": "string", "format": "uuid"},
            "run_id": {"type": "string", "format": "uuid"},
            "stage_id": {"type": "string", "pattern": _IDENTIFIER_PATTERN},
            "inputs": {"type": "array", "items": _artifact_reference_schema()},
            "expected_outputs": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["role", "relative_path"],
                    "properties": {
                        "role": {"type": "string", "pattern": _IDENTIFIER_PATTERN},
                        "relative_path": {
                            "type": "string",
                            "pattern": _RELATIVE_PATH_PATTERN,
                        },
                    },
                },
            },
            "parameters": {"type": "object"},
            "cancellation_token_relative_path": {
                "type": "string",
                "pattern": _RELATIVE_PATH_PATTERN,
            },
            "redaction_policy_version": {"type": "integer", "minimum": 1},
        },
    }


def _validation_report_schema() -> dict[str, Any]:
    finding = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "code",
            "severity",
            "message_key",
            "blocking",
            "automatic_repair_available",
        ],
        "properties": {
            "code": {"type": "string", "pattern": "^[A-Z][A-Z0-9_]{2,127}$"},
            "severity": {"enum": ["info", "warning", "error"]},
            "message_key": {"type": "string", "pattern": _IDENTIFIER_PATTERN},
            "blocking": {"type": "boolean"},
            "automatic_repair_available": {"type": "boolean"},
            "measured_value": {"type": ["number", "integer", "string", "null"]},
            "threshold": {"type": ["number", "integer", "string", "null"]},
            "geometry_reference": {
                "type": ["string", "null"],
                "pattern": _IDENTIFIER_PATTERN,
            },
        },
    }
    return {
        "$schema": _SCHEMA_URI,
        "$id": "https://minifigure3dstudio.local/schemas/validation-report-v1.json",
        "title": "MiniFigure Validation Report",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "schema_version",
            "report_id",
            "artifact_id",
            "created_at",
            "validator_versions",
            "findings",
            "status",
            "export_blocked",
            "recommended_orientation",
            "support_requirement",
        ],
        "properties": {
            "schema_version": {"const": VALIDATION_REPORT_SCHEMA_VERSION},
            "report_id": {"type": "string", "format": "uuid"},
            "artifact_id": {"type": "string", "format": "uuid"},
            "created_at": {"type": "string", "format": "date-time"},
            "validator_versions": {
                "type": "object",
                "minProperties": 1,
                "additionalProperties": {"type": "string", "minLength": 1},
            },
            "metrics": {"type": "object"},
            "findings": {"type": "array", "items": finding},
            "status": {
                "enum": ["ready_to_print", "ready_with_warnings", "repair_required"]
            },
            "export_blocked": {"type": "boolean"},
            "recommended_orientation": {"type": "string", "minLength": 1},
            "support_requirement": {"enum": ["none", "low", "medium", "high"]},
        },
    }


def schemas() -> dict[str, dict[str, Any]]:
    project = _pydantic_schema(Project)
    project["$id"] = "https://minifigure3dstudio.local/schemas/project-v1.json"
    engine = _pydantic_schema(EngineManifest)
    engine["$id"] = "https://minifigure3dstudio.local/schemas/engine-manifest-v1.json"
    worker_result = _pydantic_schema(StageResult)
    worker_result["$id"] = "https://minifigure3dstudio.local/schemas/worker-result-v1.json"
    return {
        "project.schema.json": project,
        "engine_manifest.schema.json": engine,
        "worker_request.schema.json": _worker_request_schema(),
        "worker_result.schema.json": worker_result,
        "validation_report.schema.json": _validation_report_schema(),
    }


def generate(output_root: Path) -> None:
    output_root.mkdir(parents=True, exist_ok=True)
    for filename, schema in schemas().items():
        target = output_root / filename
        target.write_text(
            json.dumps(schema, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def _parse_args() -> argparse.Namespace:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-root",
        type=Path,
        default=project_root / "app" / "config" / "schemas",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    output_root = args.output_root.resolve()
    generate(output_root)
    print(output_root)


if __name__ == "__main__":
    main()
