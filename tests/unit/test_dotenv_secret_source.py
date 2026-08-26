from __future__ import annotations

import os
from pathlib import Path

import pytest

from app.adapters.security.dotenv_secret_source import DotenvSecretSource
from app.ports.secret_store import SecretValue

_API_KEY_NAME = "MINIFIGURE_EXTERNAL_" + "API_KEY"


class FakeSecretStore:
    def __init__(self) -> None:
        self.values: dict[str, str] = {}

    def store(self, reference_id: str, secret: SecretValue) -> None:
        self.values[reference_id] = secret.reveal_text()

    def read(self, reference_id: str) -> SecretValue:
        return SecretValue(self.values[reference_id])

    def delete(self, reference_id: str) -> bool:
        return self.values.pop(reference_id, None) is not None

    def contains(self, reference_id: str) -> bool:
        return reference_id in self.values


def _write_env(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")
    path.chmod(0o600)


def test_dotenv_read_does_not_mutate_environment_or_interpolate(tmp_path: Path) -> None:
    path = tmp_path / ".env"
    _write_env(
        path,
        f"{_API_KEY_NAME}=${{HOME}}-literal\nMINIFIGURE_SECOND=two\n",
    )
    original = os.environ.get(_API_KEY_NAME)
    source = DotenvSecretSource(path)
    assert source.available_names() == (
        _API_KEY_NAME,
        "MINIFIGURE_SECOND",
    )
    with source.read(_API_KEY_NAME) as secret:
        assert secret.reveal_text() == "${HOME}-literal"
    assert os.environ.get(_API_KEY_NAME) == original


def test_dotenv_import_uses_opaque_reference(tmp_path: Path) -> None:
    path = tmp_path / ".env"
    _write_env(path, f"{_API_KEY_NAME}=runtime-test-value\n")
    store = FakeSecretStore()
    DotenvSecretSource(path).import_to_store(
        _API_KEY_NAME,
        "provider.example.primary",
        store,
    )
    assert store.values == {"provider.example.primary": "runtime-test-value"}


def test_dotenv_rejects_unapproved_variable_name(tmp_path: Path) -> None:
    path = tmp_path / ".env"
    _write_env(path, "UNRELATED_SECRET=value\n")
    with pytest.raises(ValueError, match="allowed prefix"):
        DotenvSecretSource(path).available_names()


def test_dotenv_rejects_symlink(tmp_path: Path) -> None:
    target = tmp_path / "real.env"
    _write_env(target, f"{_API_KEY_NAME}=value\n")
    link = tmp_path / ".env"
    try:
        link.symlink_to(target)
    except OSError as error:
        pytest.skip(f"symlink creation is unavailable: {error}")
    with pytest.raises(ValueError, match="regular file"):
        DotenvSecretSource(link).available_names()


@pytest.mark.skipif(os.name == "nt", reason="POSIX permission bits do not apply")
def test_dotenv_rejects_group_or_other_permissions(tmp_path: Path) -> None:
    path = tmp_path / ".env"
    path.write_text(f"{_API_KEY_NAME}=value\n", encoding="utf-8")
    path.chmod(0o644)
    with pytest.raises(PermissionError, match="group or others"):
        DotenvSecretSource(path).available_names()
