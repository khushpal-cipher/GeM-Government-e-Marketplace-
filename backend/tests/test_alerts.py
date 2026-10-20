"""Step 1.2: the daily GeM check. He pastes text from his own GeM account; the app finds bid and
contract numbers and dates, shows them back, and keeps each as an alert with its due date."""

from __future__ import annotations

from datetime import date

import pytest
from fastapi.testclient import TestClient

from gem_assistant.api.app import create_app
from gem_assistant.domain.gem_alerts import KINDS, parse_paste

CLARIFICATION = """Clarification History
Bid No: GEM/2026/B/6123456
Request no 4411, General clarification, last date to respond 24-10-2026
Please submit OEM turnover for last 3 years and OEM authorisation.
Status: Pending

Bid No: gem/2026/b/6199999
Please submit GST certificate by 26 Oct 2026"""


def test_each_bid_number_becomes_one_item_with_its_own_date_and_text():
    first, second = parse_paste("clarification", CLARIFICATION)
    assert (first.ref, first.due) == ("GEM/2026/B/6123456", date(2026, 10, 24))
    assert "OEM authorisation" in first.text and "GST" not in first.text
    assert (second.ref, second.due) == ("GEM/2026/B/6199999", date(2026, 10, 26))


@pytest.mark.parametrize("written", ["24-10-2026", "24/10/2026", "24 Oct 2026", "24-Oct-2026", "2026-10-24",
                                     "24th October 2026"])
def test_the_date_formats_gem_shows(written):
    (item,) = parse_paste("delivery", f"Contract GEMC-511687724 expected delivery {written}")
    assert (item.ref, item.due) == ("GEMC-511687724", date(2026, 10, 24))


@pytest.mark.parametrize("kind, written, due", [
    ("acceptance", "10-10-2026", date(2026, 10, 15)),   # 120 hours = 5 days from the order
    ("payment", "10-10-2026", date(2026, 10, 20)),      # 10 days after CRAC
    ("scn", "10-10-2026", date(2026, 10, 20)),          # 10 days after the notice
    ("clarification", "10-10-2026", date(2026, 10, 10)),  # the last date itself
    ("delivery", "10-10-2026", date(2026, 10, 10)),
])
def test_the_due_date_follows_the_gem_rule_for_that_kind(kind, written, due):
    (item,) = parse_paste(kind, f"GEMC-511687724 {written}")
    assert item.due == due


def test_text_without_a_date_is_kept_and_marked_unclear_never_guessed():
    (item,) = parse_paste("clarification", "Bid GEM/2026/B/6123456 pending")
    assert item.due is None and "no date" in item.unclear


def test_text_without_a_number_is_one_item_he_can_fix():
    (item,) = parse_paste("scn", "show cause notice received 10-10-2026")
    assert item.ref == "" and item.due == date(2026, 10, 20) and "no bid or contract number" in item.unclear


def test_nothing_pasted_gives_nothing():
    assert parse_paste("scn", "   \n ") == []


def test_every_kind_says_what_where_and_what_happens_if_missed():
    assert set(KINDS) == {"clarification", "acceptance", "delivery", "payment", "scn"}
    for kind in KINDS.values():
        assert kind.where and kind.if_missed and kind.label


@pytest.fixture
def client(container):
    return TestClient(create_app(container, allowed_hosts=frozenset({"testserver"})))


def _save(client, kind="clarification", ref="GEM/2026/B/6123456", due="2026-10-24", text="OEM turnover"):
    return client.post("/api/alerts", json={"kind": kind, "items": [{"ref": ref, "text": text, "due": due}]})


def test_preview_saves_nothing_and_confirming_saves(client):
    items = client.post("/api/alerts/preview", json={"kind": "clarification", "text": CLARIFICATION}).json()
    assert len(items) == 2 and client.get("/api/alerts").json() == []
    assert _save(client).json() == {"added": 1}
    (alert,) = client.get("/api/alerts").json()
    assert alert["ref"] == "GEM/2026/B/6123456" and alert["due"] == "2026-10-24"
    assert alert["where"].startswith("Bids") and alert["if_missed"]


def test_the_same_alert_is_not_saved_twice(client):
    _save(client)
    assert _save(client).json() == {"added": 0}


def test_alerts_come_most_urgent_first_and_show_the_deadline_in_words(client, clock):
    today = clock.now().date()
    _save(client, ref="GEMC-1", due=str(today.replace(year=today.year + 1)))
    _save(client, ref="GEMC-2", due=str(today.replace(year=today.year - 1)))
    _save(client, ref="GEMC-3", due=None)
    alerts = client.get("/api/alerts").json()
    assert [a["ref"] for a in alerts] == ["GEMC-2", "GEMC-1", "GEMC-3"]  # overdue, later, date unknown last
    assert alerts[0]["due_text"].startswith("missed:") and alerts[2]["due_text"] == "date unknown"


def test_a_finished_alert_leaves_the_list(client):
    _save(client)
    (alert,) = client.get("/api/alerts").json()
    assert client.post(f"/api/alerts/{alert['id']}/done").status_code == 200
    assert client.get("/api/alerts").json() == []
    assert client.post("/api/alerts/999/done").status_code == 404


def test_an_unknown_kind_is_refused(client):
    assert client.post("/api/alerts/preview", json={"kind": "lottery", "text": "x"}).status_code == 422


def test_the_page_can_ask_which_kinds_there_are(client):
    kinds = client.get("/api/alerts/kinds").json()
    assert set(kinds) == set(KINDS) and kinds["scn"]["ask"]
