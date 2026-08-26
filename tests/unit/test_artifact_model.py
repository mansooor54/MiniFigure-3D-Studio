from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

import pytest
from pydantic import ValidationError

from app.models.mesh_artifact import MeshArtifact, MeshDimensions, MeshFormat

_NOW = datetime(2026, 1, 1, tzinfo=UTC)
_HASH = "c" * 64


def _artifact(**updates: object) -> MeshArtifact:
    values: dict[str, object] = {
        "artifact_id": UUID(int=1),
        "role": "processed_mesh",
        "format": MeshFormat.GLB,
        "relative_path": "artifacts/processed/model.glb",
        "sha256": _HASH,
        "byte_size": 1024,
        "created_at": _NOW,
        "producer_id": "blender.pipeline",
        "source_run_id": UUID(int=2),
        "source_stage_id": "mesh_cleanup",
        "dimensions_mm": MeshDimensions(x_mm=40.0, y_mm=35.0, z_mm=100.0),
        "polygon_count": 50_000,
    }
    values.update(updates)
    return MeshArtifact.model_validate(values)


def test_mesh_artifact_records_reproducible_provenance() -> None:
    artifact = _artifact()
    assert artifact.unit == "millimeter"
    assert artifact.dimensions_mm is not None
    assert artifact.dimensions_mm.z_mm == 100.0


def test_mesh_artifact_rejects_project_escape_path() -> None:
    with pytest.raises(ValidationError, match="inside the project root"):
        _artifact(relative_path="../outside.glb")


def test_mesh_artifact_rejects_invalid_hash() -> None:
    with pytest.raises(ValidationError, match="SHA-256"):
        _artifact(sha256="not-a-hash")


def test_mesh_artifact_cannot_parent_itself() -> None:
    with pytest.raises(ValidationError, match="own parent"):
        _artifact(parent_artifact_id=UUID(int=1))


def test_mesh_dimensions_reject_non_finite_value() -> None:
    with pytest.raises(ValidationError):
        MeshDimensions(x_mm=float("inf"), y_mm=10.0, z_mm=20.0)
