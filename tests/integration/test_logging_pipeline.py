from __future__ import annotations

import json
import logging
from pathlib import Path

from app.logging.configure_logging import (
    LoggingConfiguration,
    configure_logging,
)
from app.logging.event_ids import EventId


def test_structured_logging_redacts_secrets_paths_and_binary_data(tmp_path: Path) -> None:
    path = tmp_path / "logs" / "application.jsonl"
    secret = "sk-" + "z" * 24
    logger = configure_logging(LoggingConfiguration(path=path))
    logger.event(
        EventId.STAGE_FAILED,
        message=f"Worker failed with Bearer {secret}",
        level=logging.ERROR,
        fields={
            "stage_id": "shape_generation",
            "api_key": secret,
            "source_path": "/Users/person/photos/front.jpg",
            "image_data": b"person bytes",
            "technical_summary": "فشل المحرك",
        },
    )
    logger.flush()
    logger.close()
    raw = path.read_text(encoding="utf-8")
    assert secret not in raw
    assert "/Users/person" not in raw
    assert "person bytes" not in raw
    payload = json.loads(raw)
    assert payload["event_id"] == EventId.STAGE_FAILED.value
    assert payload["level"] == "error"
    assert payload["fields"]["stage_id"] == "shape_generation"
    assert payload["fields"]["technical_summary"] == "فشل المحرك"


def test_logging_configuration_rejects_invalid_retention(tmp_path: Path) -> None:
    configuration = LoggingConfiguration(
        path=tmp_path / "application.jsonl",
        maximum_bytes=0,
    )
    try:
        configure_logging(configuration)
    except ValueError as error:
        assert "retention" in str(error)
    else:
        raise AssertionError("invalid logging configuration was accepted")
