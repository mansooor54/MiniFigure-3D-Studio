from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Final

from app.logging.event_ids import EventId
from app.logging.redaction_policy import RedactionPolicy

_LOGGER_NAME: Final[str] = "minifigure"


@dataclass(frozen=True)
class LoggingConfiguration:
    path: Path
    maximum_bytes: int = 2 * 1024 * 1024
    backup_count: int = 3
    level: int = logging.INFO


class SafeJsonFormatter(logging.Formatter):
    def __init__(self, policy: RedactionPolicy) -> None:
        super().__init__()
        self._policy = policy

    def format(self, record: logging.LogRecord) -> str:
        raw_fields = getattr(record, "safe_event_fields", {})
        fields = self._policy.redact_fields(raw_fields if isinstance(raw_fields, dict) else {})
        payload = {
            "recorded_at": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname.lower(),
            "event_id": getattr(record, "event_id", "logging.unknown"),
            "message": self._policy.redact_text(record.getMessage()),
            "fields": fields,
        }
        return json.dumps(payload, ensure_ascii=False, sort_keys=True, allow_nan=False)


class StructuredLogger:
    def __init__(self, logger: logging.Logger) -> None:
        self._logger = logger

    def event(
        self,
        event_id: EventId,
        *,
        message: str,
        level: int = logging.INFO,
        fields: dict[str, object] | None = None,
    ) -> None:
        self._logger.log(
            level,
            message,
            extra={
                "event_id": event_id.value,
                "safe_event_fields": fields or {},
            },
        )

    def flush(self) -> None:
        for handler in self._logger.handlers:
            handler.flush()

    def close(self) -> None:
        for handler in tuple(self._logger.handlers):
            handler.flush()
            handler.close()
            self._logger.removeHandler(handler)


def configure_logging(
    configuration: LoggingConfiguration,
    policy: RedactionPolicy | None = None,
) -> StructuredLogger:
    if configuration.maximum_bytes <= 0 or configuration.backup_count < 0:
        raise ValueError("logging retention values are invalid")
    configuration.path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(_LOGGER_NAME)
    logger.setLevel(configuration.level)
    logger.propagate = False
    for handler in tuple(logger.handlers):
        handler.close()
        logger.removeHandler(handler)
    file_handler = RotatingFileHandler(
        configuration.path,
        maxBytes=configuration.maximum_bytes,
        backupCount=configuration.backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(SafeJsonFormatter(policy or RedactionPolicy()))
    logger.addHandler(file_handler)
    return StructuredLogger(logger)
