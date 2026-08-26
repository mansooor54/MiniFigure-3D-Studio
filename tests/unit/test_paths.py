from __future__ import annotations

from pathlib import Path

from app.application_info import PRODUCT_ID
from app.config.paths import ProjectLayout, default_app_paths, product_namespace


def test_project_layout_is_human_inspectable_and_rooted(tmp_path: Path) -> None:
    root = tmp_path / "مشروع MiniFigure"
    layout = ProjectLayout(root)
    assert layout.manifest == root / "project.json"
    assert layout.journal == root / "journal.jsonl"
    assert layout.inputs_originals == root / "inputs" / "originals"
    assert layout.artifacts_processed == root / "artifacts" / "processed"
    assert layout.staging == root / ".staging"
    for directory in layout.managed_directories():
        assert directory.is_relative_to(root)


def test_project_layout_does_not_create_directories(tmp_path: Path) -> None:
    root = tmp_path / "uncreated"
    layout = ProjectLayout(root)
    assert layout.managed_directories()
    assert not root.exists()


def test_default_app_paths_share_one_data_root() -> None:
    paths = default_app_paths()
    assert paths.projects_root.parent == paths.data_root
    assert paths.engines_root.parent == paths.data_root
    assert paths.models_root.parent == paths.data_root
    assert paths.logs_root.parent == paths.data_root
    assert paths.cache_root != paths.data_root


def test_product_namespace_is_stable() -> None:
    assert product_namespace() == PRODUCT_ID
