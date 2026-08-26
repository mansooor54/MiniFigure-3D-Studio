from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.models.engine_manifest import (
    EngineFile,
    EngineLicense,
    EngineManifest,
    EngineType,
    SelfTestDefinition,
)
from app.models.generator_capabilities import (
    DeviceMode,
    GeneratorCapabilities,
    ResourceRequirements,
)
from app.models.mesh_artifact import MeshFormat

_HASH = "e" * 64


def _resources() -> ResourceRequirements:
    return ResourceRequirements(
        minimum_ram_mb=16_384,
        minimum_vram_mb=10_240,
        minimum_disk_mb=20_480,
    )


def _capabilities(adapter_id: str = "fake.generator") -> GeneratorCapabilities:
    return GeneratorCapabilities(
        adapter_id=adapter_id,
        adapter_version="1.0.0",
        minimum_image_count=1,
        maximum_image_count=1,
        supports_multi_image_conditioning=False,
        supports_textures=False,
        supports_seed=True,
        supports_pause=False,
        supports_cancel=True,
        supported_device_modes=(DeviceMode.AUTOMATIC, DeviceMode.GPU),
        supported_style_ids=("realistic_full_body",),
        output_formats=(MeshFormat.GLB,),
        resources=_resources(),
    )


def _manifest(**updates: object) -> EngineManifest:
    values: dict[str, object] = {
        "engine_id": "fake.generator",
        "display_name": "Synthetic Generator",
        "engine_type": EngineType.GENERATOR,
        "version": "1.0.0",
        "protocol_version": 1,
        "source_url": "https://example.invalid/fake-generator",
        "package_sha256": _HASH,
        "executable_relative_path": "bin/fake-generator",
        "license": EngineLicense(
            identifier="MIT",
            license_text_sha256=_HASH,
            acceptance_required=False,
            redistribution_allowed=True,
            commercial_use_allowed=True,
            excluded_territories=(),
        ),
        "resources": _resources(),
        "generator_capabilities": _capabilities(),
        "files": (
            EngineFile(relative_path="bin/fake-generator", sha256=_HASH, size_bytes=128),
        ),
        "self_test": SelfTestDefinition(
            entrypoint_relative_path="bin/fake-generator",
            arguments=("--self-test",),
            timeout_seconds=30,
            expected_result_relative_path="self-test/result.json",
        ),
    }
    values.update(updates)
    return EngineManifest.model_validate(values)


def test_generator_manifest_binds_capabilities_to_engine_id() -> None:
    manifest = _manifest()
    assert manifest.schema_version == 1
    assert manifest.generator_capabilities is not None
    assert manifest.generator_capabilities.adapter_id == manifest.engine_id


def test_generator_manifest_rejects_mismatched_adapter_id() -> None:
    with pytest.raises(ValidationError, match="adapter_id must match"):
        _manifest(generator_capabilities=_capabilities("another.generator"))


def test_non_generator_rejects_generator_capabilities() -> None:
    with pytest.raises(ValidationError, match="non-generator"):
        _manifest(engine_type=EngineType.BLENDER)


def test_license_rejects_overlapping_territories() -> None:
    with pytest.raises(ValidationError, match="cannot overlap"):
        EngineLicense(
            identifier="Restricted-Test",
            license_text_sha256=_HASH,
            acceptance_required=True,
            redistribution_allowed=False,
            commercial_use_allowed=True,
            allowed_territories=("AE",),
            excluded_territories=("AE",),
        )


def test_model_hash_requires_revision() -> None:
    with pytest.raises(ValidationError, match="requires model_revision"):
        _manifest(model_sha256=_HASH)
