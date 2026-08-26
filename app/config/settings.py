from __future__ import annotations

import json
from enum import StrEnum
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator, model_validator

from app.adapters.filesystem.atomic_file_writer import AtomicFileWriter
from app.models._base import DomainModel, validate_identifier
from app.models.generator_capabilities import DeviceMode
from app.models.project import ProjectLocale


class ThemePreference(StrEnum):
    SYSTEM = "system"
    DARK = "dark"


class SecretReference(DomainModel):
    provider_id: str
    reference_id: str

    @field_validator("provider_id", "reference_id")
    @classmethod
    def validate_ids(cls, value: str) -> str:
        return validate_identifier(value)


class LocalSettings(DomainModel):
    schema_version: Literal[1] = 1
    locale: ProjectLocale = ProjectLocale.ENGLISH
    theme: ThemePreference = ThemePreference.DARK
    ui_scale: float = Field(default=1.0, ge=0.8, le=2.0)
    projects_root: str | None = None
    preferred_device_mode: DeviceMode = DeviceMode.AUTOMATIC
    external_network_enabled: bool = False
    enabled_provider_ids: tuple[str, ...] = ()
    secret_references: tuple[SecretReference, ...] = ()
    telemetry_enabled: Literal[False] = False
    log_retention_days: int = Field(default=14, ge=0, le=365)
    maximum_log_megabytes: int = Field(default=20, ge=1, le=1024)
    preserve_imported_originals: bool = True

    @field_validator("enabled_provider_ids")
    @classmethod
    def validate_provider_ids(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        normalized = tuple(validate_identifier(value) for value in values)
        if len(normalized) != len(set(normalized)):
            raise ValueError("enabled provider IDs must be unique")
        return normalized

    @field_validator("projects_root")
    @classmethod
    def validate_projects_root(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if not value or any(not character.isprintable() for character in value):
            raise ValueError("projects_root must be a printable path")
        return value

    @model_validator(mode="after")
    def validate_secret_references(self) -> LocalSettings:
        providers = [reference.provider_id for reference in self.secret_references]
        if len(providers) != len(set(providers)):
            raise ValueError("secret references must be unique per provider")
        return self


class LocalSettingsStore:
    def __init__(self, settings_root: Path) -> None:
        self._settings_root = settings_root.resolve(strict=False)
        self._path = self._settings_root / "settings.json"
        self._writer = AtomicFileWriter(self._settings_root)

    def load(self) -> LocalSettings:
        if not self._path.exists():
            return LocalSettings()
        if self._path.is_symlink() or self._path.stat().st_size > 1024 * 1024:
            raise ValueError("settings file is unsafe or oversized")
        payload = json.loads(self._path.read_text(encoding="utf-8"))
        return LocalSettings.model_validate(payload)

    def save(self, settings: LocalSettings) -> None:
        def validate(path: Path) -> None:
            payload = json.loads(path.read_text(encoding="utf-8"))
            LocalSettings.model_validate(payload)

        self._writer.write_json(
            self._path,
            settings.model_dump(mode="json"),
            validate=validate,
        )
