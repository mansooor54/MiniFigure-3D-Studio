from __future__ import annotations

import platform

import pytest

from app.adapters.security.windows_credential_store import WindowsCredentialStore
from app.ports.secret_store import SecretStoreError, SecretValue


class FakeCredentialBackend:
    def __init__(self) -> None:
        self.values: dict[tuple[str, str], str] = {}

    def set_password(self, service: str, username: str, password: str) -> None:
        self.values[(service, username)] = password

    def get_password(self, service: str, username: str) -> str | None:
        return self.values.get((service, username))

    def delete_password(self, service: str, username: str) -> None:
        del self.values[(service, username)]


def test_secret_value_closes_after_context() -> None:
    secret = SecretValue("runtime-test-value")
    with secret as active:
        assert active.reveal_text() == "runtime-test-value"
    assert secret.closed is True
    with pytest.raises(SecretStoreError, match="closed"):
        secret.reveal_text()


def test_injected_credential_backend_satisfies_store_contract() -> None:
    backend = FakeCredentialBackend()
    store = WindowsCredentialStore(backend=backend)
    with SecretValue("runtime-test-value") as secret:
        store.store("provider.example.primary", secret)
    assert store.contains("provider.example.primary") is True
    with store.read("provider.example.primary") as loaded:
        assert loaded.reveal_text() == "runtime-test-value"
    assert store.delete("provider.example.primary") is True
    assert store.delete("provider.example.primary") is False


def test_missing_credential_read_is_explicit_failure() -> None:
    store = WindowsCredentialStore(backend=FakeCredentialBackend())
    with pytest.raises(SecretStoreError, match="not found"):
        store.read("provider.example.primary")


@pytest.mark.skipif(platform.system() == "Windows", reason="non-Windows behavior only")
def test_native_windows_backend_discovery_is_refused_off_windows() -> None:
    with pytest.raises(SecretStoreError, match="unavailable"):
        WindowsCredentialStore()
