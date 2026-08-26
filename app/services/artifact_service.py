from __future__ import annotations

import os
import shutil
from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from uuid import UUID

from app.adapters.filesystem.artifact_hasher import ArtifactHasher
from app.adapters.filesystem.atomic_file_writer import AtomicFileWriter
from app.adapters.filesystem.reparse_point_guard import assert_no_reparse_points
from app.adapters.filesystem.safe_paths import project_relative_path, resolve_project_child
from app.models.mesh_artifact import MeshArtifact, MeshDimensions, MeshFormat
from app.ports.clock import Clock

ArtifactValidator = Callable[[Path], None]


class ArtifactGroup(StrEnum):
    RAW = "raw"
    PROCESSED = "processed"


@dataclass(frozen=True)
class StagedArtifact:
    artifact_id: UUID
    role: str
    format: MeshFormat
    relative_path: str
    sha256: str
    byte_size: int


class ArtifactService:
    def __init__(self, project_root: Path, clock: Clock) -> None:
        self._project_root = project_root.resolve(strict=False)
        self._clock = clock
        self._hasher = ArtifactHasher(self._project_root)
        self._writer = AtomicFileWriter(self._project_root)

    def stage_file(
        self,
        source: Path,
        *,
        artifact_id: UUID,
        role: str,
        mesh_format: MeshFormat,
        maximum_bytes: int,
        validate: ArtifactValidator,
    ) -> StagedArtifact:
        if source.is_symlink() or not source.is_file():
            raise ValueError("artifact source must be a regular file")
        source_size = source.stat().st_size
        if source_size <= 0 or source_size > maximum_bytes:
            raise ValueError("artifact source size is outside the declared limit")
        relative = f".staging/artifacts/{artifact_id.hex}/{role}.{mesh_format.value}"
        staged = resolve_project_child(self._project_root, relative)
        staged.parent.mkdir(parents=True, exist_ok=False)
        assert_no_reparse_points(self._project_root, staged)
        try:
            with source.open("rb") as input_handle, staged.open("xb") as output_handle:
                shutil.copyfileobj(input_handle, output_handle, length=1024 * 1024)
                output_handle.flush()
                os.fsync(output_handle.fileno())
            validate(staged)
            hashed = self._hasher.hash_file(staged, maximum_bytes=maximum_bytes)
            return StagedArtifact(
                artifact_id=artifact_id,
                role=role,
                format=mesh_format,
                relative_path=project_relative_path(self._project_root, staged),
                sha256=hashed.sha256,
                byte_size=hashed.byte_size,
            )
        except Exception:
            shutil.rmtree(staged.parent, ignore_errors=True)
            raise

    def promote(
        self,
        staged: StagedArtifact,
        *,
        group: ArtifactGroup,
        source_run_id: UUID,
        source_stage_id: str,
        producer_id: str,
        parent_artifact_id: UUID | None = None,
        dimensions_mm: MeshDimensions | None = None,
        polygon_count: int = 0,
    ) -> MeshArtifact:
        source = resolve_project_child(self._project_root, staged.relative_path)
        current_hash = self._hasher.hash_file(source, maximum_bytes=staged.byte_size)
        if current_hash.sha256 != staged.sha256 or current_hash.byte_size != staged.byte_size:
            raise ValueError("staged artifact changed after validation")
        relative = (
            f"artifacts/{group.value}/{staged.role}-{staged.artifact_id.hex}."
            f"{staged.format.value}"
        )
        destination = resolve_project_child(self._project_root, relative)
        destination.parent.mkdir(parents=True, exist_ok=True)
        assert_no_reparse_points(self._project_root, destination)
        if destination.exists():
            raise FileExistsError(destination)
        os.replace(source, destination)
        try:
            promoted_hash = self._hasher.hash_file(destination, maximum_bytes=staged.byte_size)
            if promoted_hash.sha256 != staged.sha256:
                raise ValueError("promoted artifact hash mismatch")
            artifact = MeshArtifact(
                artifact_id=staged.artifact_id,
                role=staged.role,
                format=staged.format,
                relative_path=relative,
                sha256=promoted_hash.sha256,
                byte_size=promoted_hash.byte_size,
                created_at=self._clock.now(),
                producer_id=producer_id,
                source_run_id=source_run_id,
                source_stage_id=source_stage_id,
                parent_artifact_id=parent_artifact_id,
                dimensions_mm=dimensions_mm,
                polygon_count=polygon_count,
            )
            metadata = destination.with_name(f"{destination.name}.artifact.json")
            self._writer.write_json(metadata, artifact.model_dump(mode="json"))
            destination.chmod(0o444)
            source.parent.rmdir()
            return artifact
        except Exception:
            destination.chmod(0o600)
            destination.unlink(missing_ok=True)
            raise
