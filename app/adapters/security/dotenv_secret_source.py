from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Final

from dotenv import dotenv_values

from app.ports.secret_store import SecretStore, SecretValue, validate_secret_reference

_VARIABLE_PATTERN: Final[re.Pattern[str]] = re.compile(r"^[A-Z][A-Z0-9_]{2,127}$")
_MAXIMUM_DOTENV_BYTES: Final[int] = 64 * 1024


class DotenvSecretSource:
    def __init__(self, path: Path, *, allowed_prefix: str = "MINIFIGURE_") -> None:
        self._path = path
        self._allowed_prefix = allowed_prefix

    def available_names(self) -> tuple[str, ...]:
        values = self._load()
        return tuple(sorted(name for name, value in values.items() if value))

    def read(self, variable_name: str) -> SecretValue:
        self._validate_variable_name(variable_name)
        value = self._load().get(variable_name)
        if value is None or value == "":
            raise KeyError(variable_name)
        return SecretValue(value)

    def import_to_store(
        self,
        variable_name: str,
        reference_id: str,
        store: SecretStore,
    ) -> None:
        validate_secret_reference(reference_id)
        with self.read(variable_name) as secret:
            store.store(reference_id, secret)

    def _load(self) -> dict[str, str | None]:
        self._validate_file()
        values = dotenv_values(
            dotenv_path=self._path,
            encoding="utf-8",
            interpolate=False,
        )
        filtered: dict[str, str | None] = {}
        for name, value in values.items():
            self._validate_variable_name(name)
            filtered[name] = value
        return filtered

    def _validate_variable_name(self, variable_name: str) -> None:
        if _VARIABLE_PATTERN.fullmatch(variable_name) is None:
            raise ValueError("secret variable name is invalid")
        if not variable_name.startswith(self._allowed_prefix):
            raise ValueError("secret variable is outside the allowed prefix")

    def _validate_file(self) -> None:
        if self._path.is_symlink() or not self._path.is_file():
            raise ValueError(".env source must be a regular file")
        if self._path.stat().st_size > _MAXIMUM_DOTENV_BYTES:
            raise ValueError(".env source exceeds the size limit")
        if os.name != "nt" and self._path.stat().st_mode & 0o077:
            raise PermissionError(".env source must not be accessible by group or others")
