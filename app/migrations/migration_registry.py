from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass

from app.application_info import PROJECT_SCHEMA_VERSION

Migration = Callable[[dict[str, object]], dict[str, object]]


class MigrationError(RuntimeError):
    """Raised when project data cannot be migrated through registered versions."""


@dataclass(frozen=True)
class MigrationStep:
    from_version: int
    to_version: int
    migrate: Migration


class MigrationRegistry:
    def __init__(self, steps: tuple[MigrationStep, ...] = ()) -> None:
        self._steps: dict[int, MigrationStep] = {}
        for step in steps:
            if step.to_version != step.from_version + 1:
                raise ValueError("migration steps must advance exactly one version")
            if step.from_version in self._steps:
                raise ValueError("migration source versions must be unique")
            self._steps[step.from_version] = step

    def migrate(
        self,
        payload: Mapping[str, object],
        *,
        target_version: int = PROJECT_SCHEMA_VERSION,
    ) -> dict[str, object]:
        working = dict(payload)
        source = working.get("schema_version")
        if not isinstance(source, int) or isinstance(source, bool):
            raise MigrationError("project schema_version must be an integer")
        if source > target_version:
            raise MigrationError("project schema is newer than this application")
        while source < target_version:
            step = self._steps.get(source)
            if step is None:
                raise MigrationError(
                    f"no migration path from schema {source} to {target_version}"
                )
            candidate = step.migrate(dict(working))
            if candidate.get("schema_version") != step.to_version:
                raise MigrationError("migration did not produce its declared schema version")
            working = candidate
            source = step.to_version
        return working

    def registered_routes(self) -> tuple[tuple[int, int], ...]:
        return tuple(
            (step.from_version, step.to_version)
            for step in sorted(self._steps.values(), key=lambda item: item.from_version)
        )
