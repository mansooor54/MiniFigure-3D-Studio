from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.config.settings import LocalSettings, LocalSettingsStore, SecretReference
from app.models.project import ProjectLocale


def test_default_settings_are_local_private_and_secret_free() -> None:
    settings = LocalSettings()
    payload = settings.model_dump(mode="json")
    assert settings.external_network_enabled is False
    assert settings.telemetry_enabled is False
    assert settings.enabled_provider_ids == ()
    assert settings.secret_references == ()
    assert not any("key" in key or "password" in key for key in payload)


def test_settings_store_round_trips_arabic_project_root(tmp_path: Path) -> None:
    store = LocalSettingsStore(tmp_path / "settings")
    settings = LocalSettings(
        locale=ProjectLocale.ARABIC,
        projects_root="/Users/example/مشاريع MiniFigure",
        enabled_provider_ids=("example.provider",),
        secret_references=(
            SecretReference(
                provider_id="example.provider",
                reference_id="provider.example.primary",
            ),
        ),
    )
    store.save(settings)
    assert store.load() == settings
    raw = (tmp_path / "settings" / "settings.json").read_text(encoding="utf-8")
    assert "مشاريع MiniFigure" in raw
    assert "api_key" not in raw


def test_unknown_secret_field_is_rejected() -> None:
    with pytest.raises(ValidationError, match="Extra inputs"):
        LocalSettings.model_validate({"api_key": "forbidden"})


def test_telemetry_cannot_be_enabled_in_stage_two_settings() -> None:
    with pytest.raises(ValidationError):
        LocalSettings.model_validate({"telemetry_enabled": True})


def test_duplicate_provider_and_secret_references_are_rejected() -> None:
    with pytest.raises(ValidationError, match="provider IDs must be unique"):
        LocalSettings(enabled_provider_ids=("example.provider", "example.provider"))
    reference = SecretReference(
        provider_id="example.provider",
        reference_id="provider.example.primary",
    )
    with pytest.raises(ValidationError, match="unique per provider"):
        LocalSettings(secret_references=(reference, reference))


def test_invalid_persisted_settings_are_not_silently_defaulted(tmp_path: Path) -> None:
    root = tmp_path / "settings"
    root.mkdir()
    (root / "settings.json").write_text(
        json.dumps({"schema_version": 99}),
        encoding="utf-8",
    )
    with pytest.raises(ValidationError):
        LocalSettingsStore(root).load()
