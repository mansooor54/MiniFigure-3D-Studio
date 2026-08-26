from __future__ import annotations

import json
import tomllib
from pathlib import Path
from typing import Final

import app
from app.application_info import (
    ENGINE_MANIFEST_SCHEMA_VERSION,
    PRODUCT_ID,
    PRODUCT_NAME,
    PROJECT_SCHEMA_VERSION,
    VALIDATION_REPORT_SCHEMA_VERSION,
    VERSION,
    WORKER_PROTOCOL_VERSION,
)

_ROOT: Final[Path] = Path(__file__).resolve().parents[2]


def test_package_version_matches_project_metadata() -> None:
    with (_ROOT / "pyproject.toml").open("rb") as handle:
        metadata = tomllib.load(handle)
    assert app.__version__ == VERSION == metadata["project"]["version"]


def test_product_identity_is_stable() -> None:
    assert PRODUCT_NAME == "MiniFigure 3D Studio"
    assert PRODUCT_ID == "com.minifigure3dstudio.desktop"


def test_generated_schema_versions_match_constants() -> None:
    schema_root = _ROOT / "app" / "config" / "schemas"
    project = json.loads((schema_root / "project.schema.json").read_text(encoding="utf-8"))
    engine = json.loads(
        (schema_root / "engine_manifest.schema.json").read_text(encoding="utf-8")
    )
    worker = json.loads(
        (schema_root / "worker_request.schema.json").read_text(encoding="utf-8")
    )
    validation = json.loads(
        (schema_root / "validation_report.schema.json").read_text(encoding="utf-8")
    )
    assert project["properties"]["schema_version"]["const"] == PROJECT_SCHEMA_VERSION
    assert engine["properties"]["schema_version"]["const"] == ENGINE_MANIFEST_SCHEMA_VERSION
    assert worker["properties"]["protocol_version"]["const"] == WORKER_PROTOCOL_VERSION
    assert (
        validation["properties"]["schema_version"]["const"]
        == VALIDATION_REPORT_SCHEMA_VERSION
    )
