from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Final
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from uuid import UUID

_REDACTED: Final[str] = "[REDACTED]"
_ABSOLUTE_PATH_REDACTED: Final[str] = "[ABSOLUTE_PATH_REDACTED]"
_SECRET_KEY_PARTS: Final[tuple[str, ...]] = (
    "authorization",
    "api_key",
    "apikey",
    "access_token",
    "refresh_token",
    "password",
    "passwd",
    "secret",
    "credential",
    "cookie",
    "set-cookie",
    "private_key",
    "environment",
    "env_dump",
)
_BINARY_KEY_PARTS: Final[tuple[str, ...]] = (
    "source_image",
    "image_data",
    "thumbnail",
    "mask_data",
    "texture_data",
    "response_body",
    "request_body",
)
_PATH_KEY_PARTS: Final[tuple[str, ...]] = (
    "absolute_path",
    "source_path",
    "original_path",
    "executable_path",
)
_TOKEN_PATTERNS: Final[tuple[re.Pattern[str], ...]] = (
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"(?i)\b(api[_-]?key|token|password|secret)=([^\s&]+)"),
)
_WINDOWS_PATH: Final[re.Pattern[str]] = re.compile(r"(?<![A-Za-z0-9])(?:[A-Za-z]:\\)[^\s\"']+")
_POSIX_PATH: Final[re.Pattern[str]] = re.compile(
    r"(?<![A-Za-z0-9])/(?:Users|home|private|tmp|var|mnt)/[^\s\"']+"
)


@dataclass(frozen=True)
class RedactionLimits:
    maximum_depth: int = 6
    maximum_items: int = 100
    maximum_string_length: int = 2000


_DEFAULT_LIMITS: Final[RedactionLimits] = RedactionLimits()


class RedactionPolicy:
    def __init__(self, limits: RedactionLimits = _DEFAULT_LIMITS) -> None:
        self._limits = limits

    def redact_fields(self, fields: Mapping[str, object]) -> dict[str, object]:
        return {
            str(key): self._redact_value(str(key), value, depth=0)
            for key, value in list(fields.items())[: self._limits.maximum_items]
        }

    def redact_text(self, value: str) -> str:
        text = value[: self._limits.maximum_string_length]
        for pattern in _TOKEN_PATTERNS:
            text = pattern.sub(self._replace_secret_match, text)
        text = _WINDOWS_PATH.sub(_ABSOLUTE_PATH_REDACTED, text)
        text = _POSIX_PATH.sub(_ABSOLUTE_PATH_REDACTED, text)
        return self._redact_url(text)

    def _redact_value(self, key: str, value: object, *, depth: int) -> object:
        normalized_key = key.casefold().replace("-", "_")
        if any(part in normalized_key for part in _SECRET_KEY_PARTS):
            return _REDACTED
        if any(part in normalized_key for part in _BINARY_KEY_PARTS):
            return _REDACTED
        if any(part in normalized_key for part in _PATH_KEY_PARTS):
            return _ABSOLUTE_PATH_REDACTED
        if depth >= self._limits.maximum_depth:
            return "[DEPTH_LIMIT]"
        if value is None or isinstance(value, bool | int | float):
            return value
        if isinstance(value, str):
            if len(value) > self._limits.maximum_string_length:
                return "[OVERSIZED_VALUE_REDACTED]"
            return self.redact_text(value)
        if isinstance(value, bytes | bytearray | memoryview):
            return _REDACTED
        if isinstance(value, Path):
            return _ABSOLUTE_PATH_REDACTED if value.is_absolute() else value.as_posix()
        if isinstance(value, UUID | datetime | date):
            return str(value)
        if isinstance(value, Mapping):
            return {
                str(item_key): self._redact_value(
                    str(item_key),
                    item_value,
                    depth=depth + 1,
                )
                for item_key, item_value in list(value.items())[: self._limits.maximum_items]
            }
        if isinstance(value, Sequence):
            return [
                self._redact_value(key, item, depth=depth + 1)
                for item in list(value)[: self._limits.maximum_items]
            ]
        return self.redact_text(str(value))

    @staticmethod
    def _replace_secret_match(match: re.Match[str]) -> str:
        prefix = match.group(1) if match.lastindex else ""
        return f"{prefix}={_REDACTED}" if prefix else _REDACTED

    @staticmethod
    def _redact_url(text: str) -> str:
        if "://" not in text:
            return text
        try:
            split = urlsplit(text)
        except ValueError:
            return text
        if not split.scheme or not split.netloc:
            return text
        query = []
        for key, value in parse_qsl(split.query, keep_blank_values=True):
            normalized = key.casefold().replace("-", "_")
            if any(part in normalized for part in _SECRET_KEY_PARTS):
                value = _REDACTED
            query.append((key, value))
        netloc = split.hostname or ""
        if split.port is not None:
            netloc = f"{netloc}:{split.port}"
        return urlunsplit((split.scheme, netloc, split.path, urlencode(query), split.fragment))
