"""Step 1.6: Import invited bids (progress.md step 1.6).

When the seller pastes notification lines from GeM (Seller dashboard -> Notifications:
"You are invited to participate in bid (GEM/...)"):
1. The app extracts bid numbers and extended dates.
2. Checks whether each bid is already known or analysed.
3. For new bids, looks up the document ID via listing search (capped at <= 10 a day, guarded).
4. Fetches and analyses the bid document.
"""

from __future__ import annotations

from datetime import date
import pytest
from fastapi.testclient import TestClient

from gem_assistant.api.app import create_app
from gem_assistant.domain.invited_bids import parse_invited_bids

SAMPLE_NOTIFICATIONS = """
Seller dashboard notifications:
Latest Bids
You are invited to participate in bid (GEM/2026/B/8001001)
bid GEM/2026/B/8001001 extended to 28-10-2026
You are invited to participate in bid (GEM/2026/B/8001002)
You are invited to participate in bid GEM/2026/B/8001003
Random announcement text here
bid GEM/2026/B/8001004 extended to 30 Oct 2026
"""


def test_parses_invited_bid_numbers_and_extended_dates():
    bids = parse_invited_bids(SAMPLE_NOTIFICATIONS)
    assert len(bids) == 4
    by_num = {b.bid_number: b for b in bids}

    assert "GEM/2026/B/8001001" in by_num
    assert by_num["GEM/2026/B/8001001"].extended_to == date(2026, 10, 28)

    assert "GEM/2026/B/8001002" in by_num
    assert by_num["GEM/2026/B/8001002"].extended_to is None

    assert "GEM/2026/B/8001003" in by_num
    assert "GEM/2026/B/8001004" in by_num
    assert by_num["GEM/2026/B/8001004"].extended_to == date(2026, 10, 30)


def test_deduplicates_repeated_bid_numbers_in_paste():
    text = """
    You are invited to participate in bid (GEM/2026/B/9991111)
    Reminder: You are invited to participate in bid (GEM/2026/B/9991111)
    """
    bids = parse_invited_bids(text)
    assert len(bids) == 1
    assert bids[0].bid_number == "GEM/2026/B/9991111"


def test_empty_or_unrelated_paste_returns_empty():
    assert parse_invited_bids("") == []
    assert parse_invited_bids("No bids here, just general notification.") == []


@pytest.fixture
def source():
    from .test_discovery import SAMPLE_DOC, FakeSource
    from .listing_fixtures import make_doc
    # GeM's search matches loosely: the bid asked for, plus one that isn't it.
    return FakeSource(docs=[make_doc(1), SAMPLE_DOC])


@pytest.fixture
def app(settings, clock, transport, source):
    from gem_assistant.container import Container
    return Container.build(settings, clock=clock, transport=transport, listing_source_factory=source.bind)


def _queue_pdf(transport):
    from .conftest import SAMPLE_PDF
    transport.queue(body=SAMPLE_PDF.read_bytes(), headers={"content-type": "application/pdf"})


def test_each_pasted_bid_says_whether_it_needs_a_lookup(app):
    items = app.invited_bids.parse(SAMPLE_NOTIFICATIONS)
    assert [i["status"] for i in items] == ["NEEDS_LOOKUP"] * 4
    assert items[0]["extended_to"] == "2026-10-28"


def test_a_lookup_downloads_only_the_exact_bid_number(app, source, transport):
    _queue_pdf(transport)
    results = app.invited_bids.import_bids(["GEM/2025/B/6819518", "GEM/2026/B/8009999"])
    found, missing = results
    assert found["status"] == "ANALYSED" and found["bid_id"]
    assert missing["status"] == "NOT_FOUND"  # never the loose match GEM/2026/B/7000001
    pdfs = [url for url, _ in transport.calls if "showbidDocument" in url]
    assert len(pdfs) == 1 and pdfs[0].endswith("/8506455")
    assert source.calls == [(["GEM/2025/B/6819518", "GEM/2026/B/8009999"], 1)]
    # Asked again: already analysed, nothing fetched.
    assert app.invited_bids.parse("bid GEM/2025/B/6819518")[0]["status"] == "ANALYSED"
    assert app.invited_bids.import_bids(["GEM/2025/B/6819518"])[0]["status"] == "ANALYSED"
    assert len(source.calls) == 1


def test_without_a_contact_email_nothing_is_fetched(app, source, settings):
    from dataclasses import replace
    from gem_assistant.config import PLACEHOLDER_CONTACT
    from gem_assistant.container import Container
    c = Container.build(replace(settings, safety=replace(settings.safety, contact_email=PLACEHOLDER_CONTACT)),
                        listing_source_factory=source.bind)
    (result,) = c.invited_bids.import_bids(["GEM/2025/B/6819518"])
    assert result["status"] == "NOT_STARTED" and "email" in result["message"].lower()
    assert source.calls == []


def test_at_most_ten_and_only_bid_numbers(app):
    with pytest.raises(ValueError, match="10"):
        app.invited_bids.import_bids([f"GEM/2026/B/{i}" for i in range(11)])
    with pytest.raises(ValueError, match="bid number"):
        app.invited_bids.import_bids(["office chair"])


def test_the_api_parses_and_refuses_too_many(app):
    client = TestClient(create_app(app, allowed_hosts=frozenset({"testserver"})))
    data = client.post("/api/bids/invited/parse", json={"text": SAMPLE_NOTIFICATIONS}).json()
    assert [i["bid_number"] for i in data["items"]][0] == "GEM/2026/B/8001001"
    too_many = [f"GEM/2026/B/{i}" for i in range(8000001, 8000015)]
    res = client.post("/api/bids/invited/import", json={"bid_numbers": too_many})
    assert res.status_code == 400 and "10" in res.json()["detail"]
