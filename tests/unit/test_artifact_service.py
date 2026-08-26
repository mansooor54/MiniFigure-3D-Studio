from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

import pytest

from app.models.mesh_artifact import MeshFormat
from app.services.artifact_service import ArtifactGroup, ArtifactService


@dataclass(frozen=True)
class FixedClock:
    value: datetime

    def now(self) -> datetime:
        return self.value


def _service(root: Path) -> ArtifactService:
    return ArtifactService(root, FixedClock(datetime(2026, 1, 1, tzinfo=UTC)))


def test_stage_and_promote_creates_immutable_artifact_and_metadata(tmp_path: Path) -> None:
    root = tmp_path / "project"
    source = tmp_path / "source.obj"
    source.write_text("v 0 0 0\nv 1 0 0\nv 0 1 0\nf 1 2 3\n", encoding="utf-8")
    service = _service(root)

    def validate_obj(path: Path) -> None:
        assert "f 1 2 3" in path.read_text(encoding="utf-8")

    staged = service.stage_file(
        source,
        artifact_id=UUID(int=1),
        role="raw_mesh",
        mesh_format=MeshFormat.OBJ,
        maximum_bytes=1024,
        validate=validate_obj,
    )
    artifact = service.promote(
        staged,
        group=ArtifactGroup.RAW,
        source_run_id=UUID(int=2),
        source_stage_id="shape_generation",
        producer_id="fake.generator",
        polygon_count=1,
    )
    destination = root / artifact.relative_path
    assert destination.read_bytes() == source.read_bytes()
    assert destination.stat().st_mode & 0o222 == 0
    assert destination.with_name(f"{destination.name}.artifact.json").is_file()
    assert not (root / ".staging" / "artifacts" / UUID(int=1).hex).exists()


def test_stage_validation_failure_removes_candidate(tmp_path: Path) -> None:
    root = tmp_path / "project"
    source = tmp_path / "source.obj"
    source.write_text("invalid", encoding="utf-8")

    def reject(_path: Path) -> None:
        raise ValueError("seeded validator failure")

    with pytest.raises(ValueError, match="seeded validator failure"):
        _service(root).stage_file(
            source,
            artifact_id=UUID(int=1),
            role="raw_mesh",
            mesh_format=MeshFormat.OBJ,
            maximum_bytes=1024,
            validate=reject,
        )
    assert not (root / ".staging" / "artifacts" / UUID(int=1).hex).exists()


def test_tampered_staged_artifact_is_not_promoted(tmp_path: Path) -> None:
    root = tmp_path / "project"
    source = tmp_path / "source.obj"
    source.write_text("v 0 0 0\n", encoding="utf-8")
    service = _service(root)
    staged = service.stage_file(
        source,
        artifact_id=UUID(int=1),
        role="raw_mesh",
        mesh_format=MeshFormat.OBJ,
        maximum_bytes=1024,
        validate=lambda _path: None,
    )
    (root / staged.relative_path).write_text("tampered", encoding="utf-8")
    with pytest.raises(ValueError, match="changed after validation"):
        service.promote(
            staged,
            group=ArtifactGroup.RAW,
            source_run_id=UUID(int=2),
            source_stage_id="shape_generation",
            producer_id="fake.generator",
        )
    assert not (root / "artifacts" / "raw").exists()


def test_empty_source_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / "empty.obj"
    source.write_bytes(b"")
    with pytest.raises(ValueError, match="size"):
        _service(tmp_path / "project").stage_file(
            source,
            artifact_id=UUID(int=1),
            role="raw_mesh",
            mesh_format=MeshFormat.OBJ,
            maximum_bytes=1024,
            validate=lambda _path: None,
        )
