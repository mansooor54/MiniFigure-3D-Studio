from __future__ import annotations

from types import TracebackType
from typing import Protocol, Self, runtime_checkable

from app.models._base import validate_identifier


class SecretStoreError(RuntimeError):
    """Raised when an operating-system credential operation fails."""


class SecretValue:
    def __init__(self, secret: str) -> None:
        if not secret:
            raise ValueError("secret cannot be empty")
        self._buffer = bytearray(secret.encode("utf-8"))
        self._closed = False

    @property
    def closed(self) -> bool:
        return self._closed

    def reveal_text(self) -> str:
        if self._closed:
            raise SecretStoreError("secret value is closed")
        return self._buffer.decode("utf-8")

    def close(self) -> None:
        for index in range(len(self._buffer)):
            self._buffer[index] = 0
        self._buffer.clear()
        self._closed = True

    def __enter__(self) -> Self:
        if self._closed:
            raise SecretStoreError("secret value is closed")
        return self

    def __exit__(
        self,
        _exception_type: type[BaseException] | None,
        _exception: BaseException | None,
        _traceback: TracebackType | None,
    ) -> None:
        self.close()


@runtime_checkable
class SecretStore(Protocol):
    def store(self, reference_id: str, secret: SecretValue) -> None:
        """Persist a secret under a validated opaque reference."""

    def read(self, reference_id: str) -> SecretValue:
        """Read a secret into a closeable, zeroizable value."""

    def delete(self, reference_id: str) -> bool:
        """Delete the referenced credential and report whether it existed."""

    def contains(self, reference_id: str) -> bool:
        """Return whether a credential exists without revealing it."""


def validate_secret_reference(reference_id: str) -> str:
    return validate_identifier(reference_id)
