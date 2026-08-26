from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from app.ports.clock import Clock, UtcSystemClock


@dataclass(frozen=True)
class FixedClock:
    value: datetime

    def now(self) -> datetime:
        return self.value


def test_fixed_clock_satisfies_protocol() -> None:
    expected = datetime(2026, 1, 1, tzinfo=UTC)
    clock: Clock = FixedClock(expected)
    assert clock.now() == expected
    assert isinstance(clock, Clock)


def test_system_clock_is_aware_utc() -> None:
    current = UtcSystemClock().now()
    assert current.tzinfo is UTC
    offset = current.utcoffset()
    assert offset is not None
    assert offset.total_seconds() == 0
