from __future__ import annotations

import importlib
import platform
from typing import Protocol, cast

from app.application_info import PRODUCT_ID
from app.ports.secret_store import (
    SecretStoreError,
    SecretValue,
    validate_secret_reference,
)


class CredentialBackend(Protocol):
    def set_password(self, service: str, username: str, password: str) -> None: ...

    def get_password(self, service: str, username: str) -> str | None: ...

    def delete_password(self, service: str, username: str) -> None: ...


class WindowsCredentialStore:
    def __init__(
        self,
        *,
        service_name: str = PRODUCT_ID,
        backend: CredentialBackend | None = None,
    ) -> None:
        self._service_name = service_name
        self._backend = backend or self._discover_windows_backend()

    def store(self, reference_id: str, secret: SecretValue) -> None:
        reference = validate_secret_reference(reference_id)
        try:
            self._backend.set_password(
                self._service_name,
                reference,
                secret.reveal_text(),
            )
        except Exception as error:
            raise SecretStoreError("credential store write failed") from error

    def read(self, reference_id: str) -> SecretValue:
        reference = validate_secret_reference(reference_id)
        try:
            value = self._backend.get_password(self._service_name, reference)
        except Exception as error:
            raise SecretStoreError("credential store read failed") from error
        if value is None:
            raise SecretStoreError("credential reference was not found")
        return SecretValue(value)

    def delete(self, reference_id: str) -> bool:
        reference = validate_secret_reference(reference_id)
        if not self.contains(reference):
            return False
        try:
            self._backend.delete_password(self._service_name, reference)
        except Exception as error:
            raise SecretStoreError("credential deletion failed") from error
        return True

    def contains(self, reference_id: str) -> bool:
        reference = validate_secret_reference(reference_id)
        try:
            return self._backend.get_password(self._service_name, reference) is not None
        except Exception as error:
            raise SecretStoreError("credential lookup failed") from error

    @staticmethod
    def _discover_windows_backend() -> CredentialBackend:
        if platform.system() != "Windows":
            raise SecretStoreError("Windows Credential Manager is unavailable")
        try:
            keyring_module = importlib.import_module("keyring")
            get_keyring = keyring_module.get_keyring
            discovered = cast(CredentialBackend, get_keyring())
        except (ImportError, AttributeError, TypeError) as error:
            raise SecretStoreError("Windows keyring backend could not be loaded") from error
        backend_name = f"{type(discovered).__module__}.{type(discovered).__name__}"
        if "Windows" not in backend_name:
            raise SecretStoreError("active keyring backend is not Windows Credential Manager")
        return discovered
