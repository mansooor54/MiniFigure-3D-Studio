from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Final

import yaml

ALGORITHM_VERSION: Final[int] = 1
IMAGE_SIZE: Final[int] = 64


@dataclass(frozen=True)
class GeneratedAsset:
    relative_path: str
    media_type: str
    purpose: str
    expected: dict[str, object]
    content: bytes


_NAVY: Final[tuple[int, int, int]] = (10, 31, 68)
_GOLD: Final[tuple[int, int, int]] = (212, 175, 55)
_WHITE: Final[tuple[int, int, int]] = (245, 247, 250)
_BLACK: Final[tuple[int, int, int]] = (0, 0, 0)


def _ppm_bytes(pixels: bytes) -> bytes:
    header = f"P6\n{IMAGE_SIZE} {IMAGE_SIZE}\n255\n".encode("ascii")
    return header + pixels


def _checker_pixels() -> bytes:
    pixels = bytearray()
    palette = (_NAVY, _GOLD, _WHITE, _BLACK)
    for y in range(IMAGE_SIZE):
        for x in range(IMAGE_SIZE):
            block = (x // 8 + y // 8) % len(palette)
            pixels.extend(palette[block])
    return bytes(pixels)


def _gradient_pixels() -> bytes:
    pixels = bytearray()
    denominator = IMAGE_SIZE - 1
    for y in range(IMAGE_SIZE):
        for x in range(IMAGE_SIZE):
            red = round(255 * x / denominator)
            green = round(255 * y / denominator)
            blue = round(255 * (x + y) / (2 * denominator))
            pixels.extend((red, green, blue))
    return bytes(pixels)


def _cube_obj() -> bytes:
    text = "# Deterministic unit cube in millimeters\n"
    text += "v -0.5 -0.5 0.0\n"
    text += "v 0.5 -0.5 0.0\n"
    text += "v 0.5 0.5 0.0\n"
    text += "v -0.5 0.5 0.0\n"
    text += "v -0.5 -0.5 1.0\n"
    text += "v 0.5 -0.5 1.0\n"
    text += "v 0.5 0.5 1.0\n"
    text += "v -0.5 0.5 1.0\n"
    text += "f 1 4 3 2\n"
    text += "f 5 6 7 8\n"
    text += "f 1 2 6 5\n"
    text += "f 2 3 7 6\n"
    text += "f 3 4 8 7\n"
    text += "f 4 1 5 8\n"
    return text.encode("ascii")


def _open_plane_obj() -> bytes:
    text = "# Deterministic open plane with one boundary loop\n"
    text += "v -1.0 -1.0 0.0\n"
    text += "v 1.0 -1.0 0.0\n"
    text += "v 1.0 1.0 0.0\n"
    text += "v -1.0 1.0 0.0\n"
    text += "f 1 2 3 4\n"
    return text.encode("ascii")


def assets() -> tuple[GeneratedAsset, ...]:
    return (
        GeneratedAsset(
            relative_path="generated/checker_64.ppm",
            media_type="image/x-portable-pixmap",
            purpose="High-frequency image-quality and deterministic decoding fixture.",
            expected={"width": IMAGE_SIZE, "height": IMAGE_SIZE, "contains_exif": False},
            content=_ppm_bytes(_checker_pixels()),
        ),
        GeneratedAsset(
            relative_path="generated/gradient_64.ppm",
            media_type="image/x-portable-pixmap",
            purpose="Exposure and intensity-distribution image fixture.",
            expected={"width": IMAGE_SIZE, "height": IMAGE_SIZE, "contains_exif": False},
            content=_ppm_bytes(_gradient_pixels()),
        ),
        GeneratedAsset(
            relative_path="generated/unit_cube.obj",
            media_type="model/obj",
            purpose="Closed synthetic mesh with known bounds and six polygon faces.",
            expected={"vertex_count": 8, "face_count": 6, "watertight": True},
            content=_cube_obj(),
        ),
        GeneratedAsset(
            relative_path="generated/open_plane.obj",
            media_type="model/obj",
            purpose="Open synthetic mesh for negative topology and repair tests.",
            expected={"vertex_count": 4, "face_count": 1, "watertight": False},
            content=_open_plane_obj(),
        ),
    )


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _manifest_entry(asset: GeneratedAsset) -> dict[str, object]:
    return {
        "path": asset.relative_path,
        "media_type": asset.media_type,
        "source": "scripts/create_synthetic_fixtures.py",
        "generator_version": ALGORITHM_VERSION,
        "license": "CC0-1.0",
        "sha256": _sha256(asset.content),
        "size_bytes": len(asset.content),
        "contains_real_person": False,
        "contains_exif": False,
        "purpose": asset.purpose,
        "expected": asset.expected,
    }


def generate(output_root: Path) -> Path:
    output_root.mkdir(parents=True, exist_ok=True)
    generated_assets = assets()
    for asset in generated_assets:
        target = output_root / asset.relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(asset.content)
    manifest = {
        "schema_version": 1,
        "policy": {
            "real_person_assets_allowed": False,
            "unmanifested_binary_assets_allowed": False,
        },
        "assets": [_manifest_entry(asset) for asset in generated_assets],
    }
    manifest_path = output_root / "asset_manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return manifest_path


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "tests" / "fixtures",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    manifest_path = generate(args.output_root.resolve())
    print(manifest_path)


if __name__ == "__main__":
    main()
