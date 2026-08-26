from __future__ import annotations

from datetime import UTC, datetime
from typing import Protocol, runtime_checkable


@runtime_checkable
class Clock(Protocol):
    def now(self) -> datetime:
        """Return an aware current timestamp."""


class UtcSystemClock:
    def now(self) -> datetime:
        return datetime.now(tz=UTC)
