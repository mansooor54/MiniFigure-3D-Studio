from __future__ import annotations

from pathlib import Path

import pytest

from app.migrations.migration_registry import (
    MigrationError,
    MigrationRegistry,
    MigrationStep,
)


def test_current_schema_returns_equal_independent_copy() -> None:
    payload: dict[str, object] = {"schema_version": 1, "project_name": "Project"}
    migrated = MigrationRegistry().migrate(payload)
    assert migrated == payload
    assert migrated is not payload


def test_future_schema_is_rejected() -> None:
    with pytest.raises(MigrationError, match="newer"):
        MigrationRegistry().migrate({"schema_version": 2})


def test_missing_migration_route_is_rejected_truthfully() -> None:
    with pytest.raises(MigrationError, match="no migration path"):
        MigrationRegistry().migrate({"schema_version": 0})


def test_registered_step_must_advance_and_produce_declared_version() -> None:
    def migrate(payload: dict[str, object]) -> dict[str, object]:
        return {**payload, "schema_version": 1}

    registry = MigrationRegistry((MigrationStep(0, 1, migrate),))
    assert registry.registered_routes() == ((0, 1),)
    assert registry.migrate({"schema_version": 0})["schema_version"] == 1


def test_invalid_migration_output_is_rejected() -> None:
    def broken(payload: dict[str, object]) -> dict[str, object]:
        return dict(payload)

    registry = MigrationRegistry((MigrationStep(0, 1, broken),))
    with pytest.raises(MigrationError, match="declared schema version"):
        registry.migrate({"schema_version": 0})


def test_no_v1_to_v2_module_exists_before_schema_v2() -> None:
    root = Path(__file__).resolve().parents[2]
    assert not (root / "app" / "migrations" / "project_v1_to_v2.py").exists()
