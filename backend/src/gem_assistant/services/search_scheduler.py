"""Runs the normal search at fixed times of day (IST) while the server is up (step 4.4).

It adds no guard rails of its own: it calls DiscoveryService.start_in_background, which already
allows one run at a time, keeps the gap between runs, and refuses while fetching is stopped.
A refused slot is simply skipped, not retried.
"""

from __future__ import annotations

import threading
from datetime import datetime, time, timedelta, timezone

from ..domain.ports import Clock
from .discovery_service import DiscoveryNotAllowed, DiscoveryService

IST = timezone(timedelta(hours=5, minutes=30))
MAX_SLOTS_PER_DAY = 4  # keeps the daily request budget (docs/build-plan.md, rule 7) honest


def parse_times(raw: str) -> tuple[time, ...]:
    """"09:00,15:00" -> times. A bad entry raises ValueError, so a typo is not silently ignored."""
    times = sorted({time.fromisoformat(part.strip()) for part in raw.split(",") if part.strip()})
    if len(times) > MAX_SLOTS_PER_DAY:
        raise ValueError(f"At most {MAX_SLOTS_PER_DAY} scheduled searches a day")
    return tuple(times)


class SearchScheduler:
    def __init__(self, discovery: DiscoveryService, clock: Clock, times: tuple[time, ...]):
        self._discovery, self._clock, self._times = discovery, clock, times
        self._done = self._latest_slot()  # a slot already past at start-up is not run late
        self._stop = threading.Event()

    def _latest_slot(self) -> datetime | None:
        now = self._clock.now().astimezone(IST)
        slots = [datetime.combine(now.date(), t, IST) for t in self._times]
        due = [s for s in slots if s <= now]
        return max(due) if due else None

    def tick(self) -> str | None:
        """Start the search if a slot has come up since the last one. Returns why not, if skipped."""
        slot = self._latest_slot()
        if slot is None or slot == self._done:
            return None
        self._done = slot  # tried once; never again for this slot, whatever the answer
        try:
            self._discovery.start_in_background(trigger="scheduled")
        except DiscoveryNotAllowed as error:
            return str(error)
        return None

    def start(self) -> None:
        def loop() -> None:
            while not self._stop.wait(30):
                self.tick()
        threading.Thread(target=loop, daemon=True, name="gem-scheduler").start()

    def stop(self) -> None:
        self._stop.set()
