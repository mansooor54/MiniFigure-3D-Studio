from __future__ import annotations

import hashlib
from pathlib import Path

import yaml

from scripts.create_synthetic_fixtures import generate
from scripts.validate_assets import load_manifest, validate_assets


def _file_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_generation_is_byte_deterministic(tmp_path: Path) -> None:
    first_root = tmp_path / "first"
    second_root = tmp_path / "second"
    generate(first_root)
    generate(second_root)
    assert _file_hashes(first_root) == _file_hashes(second_root)


def test_generated_manifest_and_assets_validate(tmp_path: Path) -> None:
    manifest_path = generate(tmp_path)
    assert validate_assets(tmp_path, manifest_path) == []


def test_unmanifested_fixture_is_rejected(tmp_path: Path) -> None:
    manifest_path = generate(tmp_path)
    rogue_file = tmp_path / "generated" / "rogue-image.png"
    rogue_file.write_bytes(b"not-a-real-image")
    issues = validate_assets(tmp_path, manifest_path)
    assert any(issue.path == "generated/rogue-image.png" for issue in issues)
    assert any("unmanifested" in issue.message for issue in issues)


def test_tampered_fixture_is_rejected(tmp_path: Path) -> None:
    manifest_path = generate(tmp_path)
    target = tmp_path / "generated" / "unit_cube.obj"
    target.write_bytes(target.read_bytes() + b"# tampered\n")
    issues = validate_assets(tmp_path, manifest_path)
    assert any(issue.path == "generated/unit_cube.obj" for issue in issues)
    assert any("does not match manifest" in issue.message for issue in issues)


def test_manifest_disables_real_person_assets(tmp_path: Path) -> None:
    manifest_path = generate(tmp_path)
    manifest = load_manifest(manifest_path)
    policy = manifest["policy"]
    assert isinstance(policy, dict)
    assert policy["real_person_assets_allowed"] is False
    assets = manifest["assets"]
    assert isinstance(assets, list)
    for entry in assets:
        assert isinstance(entry, dict)
        assert entry["contains_real_person"] is False


def test_real_person_flag_is_rejected(tmp_path: Path) -> None:
    manifest_path = generate(tmp_path)
    manifest = load_manifest(manifest_path)
    assets = manifest["assets"]
    assert isinstance(assets, list)
    first_asset = assets[0]
    assert isinstance(first_asset, dict)
    first_asset["contains_real_person"] = True
    manifest_path.write_text(
        yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    issues = validate_assets(tmp_path, manifest_path)
    assert any("contains_real_person must be false" in issue.message for issue in issues)
