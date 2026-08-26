from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from platformdirs import user_cache_path, user_data_path

from app.application_info import PRODUCT_ID, PRODUCT_NAME


@dataclass(frozen=True)
class AppPaths:
    data_root: Path
    cache_root: Path
    projects_root: Path
    engines_root: Path
    models_root: Path
    logs_root: Path


@dataclass(frozen=True)
class ProjectLayout:
    root: Path

    @property
    def manifest(self) -> Path:
        return self.root / "project.json"

    @property
    def journal(self) -> Path:
        return self.root / "journal.jsonl"

    @property
    def staging(self) -> Path:
        return self.root / ".staging"

    @property
    def inputs_originals(self) -> Path:
        return self.root / "inputs" / "originals"

    @property
    def inputs_metadata(self) -> Path:
        return self.root / "inputs" / "metadata"

    @property
    def masks(self) -> Path:
        return self.root / "masks"

    @property
    def runs(self) -> Path:
        return self.root / "runs"

    @property
    def artifacts_raw(self) -> Path:
        return self.root / "artifacts" / "raw"

    @property
    def artifacts_processed(self) -> Path:
        return self.root / "artifacts" / "processed"

    @property
    def reports(self) -> Path:
        return self.root / "reports"

    @property
    def exports(self) -> Path:
        return self.root / "exports"

    @property
    def logs(self) -> Path:
        return self.root / "logs"

    def managed_directories(self) -> tuple[Path, ...]:
        return (
            self.inputs_originals,
            self.inputs_metadata,
            self.masks,
            self.runs,
            self.artifacts_raw,
            self.artifacts_processed,
            self.reports,
            self.exports,
            self.logs,
            self.staging,
        )


def default_app_paths() -> AppPaths:
    data_root = user_data_path(PRODUCT_NAME, appauthor=False, ensure_exists=False)
    cache_root = user_cache_path(PRODUCT_NAME, appauthor=False, ensure_exists=False)
    return AppPaths(
        data_root=data_root,
        cache_root=cache_root,
        projects_root=data_root / "projects",
        engines_root=data_root / "engines",
        models_root=data_root / "models",
        logs_root=data_root / "logs",
    )


def product_namespace() -> str:
    return PRODUCT_ID
