from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

import pytest
from pydantic import ValidationError

from app.models.source_image import SourceImage

_NOW = datetime(2026, 1, 1, tzinfo=UTC)
_HASH = "d" * 64


def _source_image(**updates: object) -> SourceImage:
    values: dict[str, object] = {
        "image_id": UUID(int=1),
        "original_display_name": "صورة أمامية.jpg",
        "imported_relative_path": "inputs/originals/image-0001.jpg",
        "normalized_relative_path": "inputs/normalized/image-0001.png",
        "sha256": _HASH,
        "media_type": "image/jpeg",
        "width_px": 2048,
        "height_px": 3072,
        "exif_orientation": 1,
        "imported_at": _NOW,
        "assigned_view_id": "front",
    }
    values.update(updates)
    return SourceImage.model_validate(values)


def test_source_image_preserves_display_name_without_using_it_as_a_path() -> None:
    image = _source_image()
    assert image.original_display_name == "صورة أمامية.jpg"
    assert image.imported_relative_path == "inputs/originals/image-0001.jpg"


def test_source_image_rejects_original_overwrite_by_derivative() -> None:
    with pytest.raises(ValidationError, match="must not overwrite"):
        _source_image(normalized_relative_path="inputs/originals/image-0001.jpg")


def test_source_image_rejects_unsafe_managed_path() -> None:
    with pytest.raises(ValidationError, match="project root"):
        _source_image(imported_relative_path="inputs/../outside.jpg")


def test_source_image_rejects_invalid_orientation() -> None:
    with pytest.raises(ValidationError):
        _source_image(exif_orientation=9)
