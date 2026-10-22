"""Step 4.4: scheduled search times; the guard rails themselves are tested in test_discovery."""

from datetime import datetime, time, timedelta, timezone

import pytest

from gem_assistant.services.discovery_service import DiscoveryNotAllowed
from gem_assistant.services.search_scheduler import IST, SearchScheduler, parse_times

NINE, THREE = time(9, 0), time(15, 0)


class Clock:
    def __init__(self, hh, mm):
        self.t = datetime(2026, 10, 23, hh, mm, tzinfo=IST).astimezone(timezone.utc)

    def now(self):
        return self.t


class Discovery:
    def __init__(self, refuse=False):
        self.started, self.refuse = [], refuse

    def start_in_background(self, trigger):
        if self.refuse:
            raise DiscoveryNotAllowed("Fetching is stopped")
        self.started.append(trigger)


def test_parse_times():
    assert parse_times("15:00, 09:00") == (NINE, THREE)
    assert parse_times("") == ()
    with pytest.raises(ValueError):
        parse_times("9am")
    with pytest.raises(ValueError):
        parse_times("01:00,02:00,03:00,04:00,05:00")


def test_runs_each_slot_once_and_not_a_missed_one_at_startup():
    clock, discovery = Clock(11, 0), Discovery()
    scheduler = SearchScheduler(discovery, clock, (NINE, THREE))
    assert scheduler.tick() is None and discovery.started == []   # 09:00 passed before start-up
    clock.t = clock.t + timedelta(hours=4, minutes=1)            # 15:01
    scheduler.tick(); scheduler.tick()
    assert discovery.started == ["scheduled"]


def test_a_refused_slot_is_skipped_not_retried():
    clock, discovery = Clock(8, 59), Discovery(refuse=True)
    scheduler = SearchScheduler(discovery, clock, (NINE,))
    clock.t += timedelta(minutes=2)
    assert "stopped" in scheduler.tick()
    discovery.refuse = False
    assert scheduler.tick() is None and discovery.started == []
