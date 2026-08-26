from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.models.generator_capabilities import (
    DeviceMode,
    GeneratorCapabilities,
    ResourceRequirements,
)
from app.models.mesh_artifact import MeshFormat


def _capabilities(**updates: object) -> GeneratorCapabilities:
    values: dict[str, object] = {
        "adapter_id": "local.single_image",
        "adapter_version": "1.0.0",
        "minimum_image_count": 1,
        "maximum_image_count": 1,
        "supports_multi_image_conditioning": False,
        "supports_textures": True,
        "supports_seed": True,
        "supports_pause": False,
        "supports_cancel": True,
        "supported_device_modes": (DeviceMode.AUTOMATIC, DeviceMode.GPU),
        "supported_style_ids": ("realistic_full_body", "chibi"),
        "output_formats": (MeshFormat.GLB,),
        "resources": ResourceRequirements(
            minimum_ram_mb=16_384,
            minimum_vram_mb=10_240,
            minimum_disk_mb=20_480,
        ),
    }
    values.update(updates)
    return GeneratorCapabilities.model_validate(values)


def test_single_image_capabilities_do_not_claim_multi_image_input() -> None:
    capabilities = _capabilities()
    assert capabilities.maximum_image_count == 1
    assert capabilities.supports_multi_image_conditioning is False


def test_multiple_images_require_explicit_conditioning_support() -> None:
    with pytest.raises(ValidationError, match="multi-image conditioning"):
        _capabilities(maximum_image_count=6)


def test_capability_collections_must_be_unique() -> None:
    with pytest.raises(ValidationError, match="supported_device_modes must be unique"):
        _capabilities(
            supported_device_modes=(DeviceMode.GPU, DeviceMode.GPU),
        )


def test_image_cardinality_must_be_ordered() -> None:
    with pytest.raises(ValidationError, match="maximum_image_count"):
        _capabilities(
            minimum_image_count=2,
            maximum_image_count=1,
            supports_multi_image_conditioning=True,
        )
