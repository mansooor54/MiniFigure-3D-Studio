from __future__ import annotations

import json
from pathlib import Path
from typing import Final

from jsonschema import Draft202012Validator, FormatChecker
from pydantic import AnyUrl

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

_ROOT: Final[Path] = Path(__file__).resolve().parents[2]
_SCHEMA_PATH: Final[Path] = (
    _ROOT / "app" / "config" / "schemas" / "engine_manifest.schema.json"
)
_HASH: Final[str] = "1" * 64


def _schema() -> dict[str, object]:
    data = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def _resources() -> ResourceRequirements:
    return ResourceRequirements(
        minimum_ram_mb=4096,
        minimum_vram_mb=0,
        minimum_disk_mb=1024,
    )


def _payload() -> dict[str, object]:
    capabilities = GeneratorCapabilities(
        adapter_id="fake.generator",
        adapter_version="1.0.0",
        minimum_image_count=1,
        maximum_image_count=1,
        supports_multi_image_conditioning=False,
        supports_textures=False,
        supports_seed=True,
        supports_pause=False,
        supports_cancel=True,
        supported_device_modes=(DeviceMode.AUTOMATIC,),
        supported_style_ids=("realistic_full_body",),
        output_formats=(MeshFormat.GLB,),
        resources=_resources(),
    )
    manifest = EngineManifest(
        engine_id="fake.generator",
        display_name="Fake Generator",
        engine_type=EngineType.GENERATOR,
        version="1.0.0",
        protocol_version=1,
        source_url=AnyUrl("https://example.invalid/fake"),
        package_sha256=_HASH,
        executable_relative_path="bin/fake",
        license=EngineLicense(
            identifier="MIT",
            license_text_sha256=_HASH,
            acceptance_required=False,
            redistribution_allowed=True,
            commercial_use_allowed=True,
        ),
        resources=_resources(),
        generator_capabilities=capabilities,
        files=(EngineFile(relative_path="bin/fake", sha256=_HASH, size_bytes=1),),
        self_test=SelfTestDefinition(
            entrypoint_relative_path="bin/fake",
            timeout_seconds=10,
            expected_result_relative_path="self-test/result.json",
        ),
    )
    return manifest.model_dump(mode="json")


def test_engine_manifest_schema_is_valid_draft_2020_12() -> None:
    Draft202012Validator.check_schema(_schema())


def test_engine_manifest_serialization_validates() -> None:
    Draft202012Validator(_schema(), format_checker=FormatChecker()).validate(_payload())


def test_engine_manifest_schema_rejects_unknown_property() -> None:
    payload = _payload()
    payload["api_key"] = "must-not-be-stored"
    validator = Draft202012Validator(_schema(), format_checker=FormatChecker())
    errors = list(validator.iter_errors(payload))
    assert any("Additional properties are not allowed" in error.message for error in errors)
