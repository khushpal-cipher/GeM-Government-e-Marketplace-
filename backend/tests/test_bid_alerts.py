"""Step 5.1: alerts worked out from bids and listings (nothing stored)."""

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from gem_assistant.domain.models import (
    Assessment, BidAnalysis, ClauseFlag, Evidence, ExtractedField, ExtractionMethod, FieldStatus, ListingEntry,
    Verdict, BidKind, DocStatus,
)
from gem_assistant.services.bid_alerts import BidAlerts

NOW = datetime(2026, 10, 23, 6, 0, tzinfo=timezone.utc)
EV = Evidence(page=1, quote="q", method=ExtractionMethod.LABEL_PARSE)


def _bid(number, end, dated=None, flags=()):
    fields = [ExtractedField(name="bid_end", label="e", status=FieldStatus.FOUND, value=end.isoformat(), evidence=EV)]
    if dated:
        fields.append(ExtractedField(name="bid_dated", label="d", status=FieldStatus.FOUND, value=dated, evidence=EV))
    bid = BidAnalysis(bid_number=number, source_name="x.pdf", sha256="a" * 64, page_count=1, unread_lines=0,
                      imported_at=NOW, flags=list(flags), fields=fields)
    return SimpleNamespace(bid=bid, assessment=Assessment(verdict=Verdict.ELIGIBLE, results=[]))


def _entry(number, ends, matched=1, new=False):
    return ListingEntry(doc_id="1", bid_number=number, kind=BidKind.BID, doc_path="p", ends_at=ends, keyword="k",
                        first_seen_at=NOW, last_seen_at=NOW, doc_status=DocStatus.PENDING,
                        matched_items=matched, total_items=1, is_new=new)


def _alerts(bids, listings):
    return BidAlerts(SimpleNamespace(list=lambda: bids),
                     SimpleNamespace(status=lambda: SimpleNamespace(listings=listings)),
                     SimpleNamespace(now=lambda: NOW)).list()


def _kinds(rows):
    return [(r["kind"], r["ref"]) for r in rows]


def test_closing_within_three_days_only():
    rows = _alerts([_bid("A", NOW + timedelta(days=2)), _bid("B", NOW + timedelta(days=4)),
                    _bid("C", NOW - timedelta(hours=1))], [])
    assert _kinds(rows) == [("bid_closing", "A")]
    assert rows[0]["id"] is None and "left" in rows[0]["due_text"]


def test_blocked_bids_do_not_nag():
    blocked = _bid("A", NOW + timedelta(days=1))
    blocked.assessment = Assessment(verdict=Verdict.BLOCKED, results=[])
    assert _alerts([blocked], []) == []


def test_representation_window_for_a_forbidden_term():
    flag = ClauseFlag(category="forbidden_brand", label="brand", evidence=EV)
    # open 10+ days from 21 Oct -> may ask until the end of 25 Oct (2 days from NOW)
    rows = _alerts([_bid("A", NOW + timedelta(days=9), dated="2026-10-21", flags=[flag]),
                    _bid("B", NOW + timedelta(days=9), dated="2026-10-21")], [])
    assert ("bid_representation", "A") in _kinds(rows) and ("bid_representation", "B") not in _kinds(rows)


def test_new_matching_bid_and_the_list_your_product_nudge():
    rows = _alerts([], [_entry("N", NOW + timedelta(days=10), new=True),      # new, plenty of time
                        _entry("L", NOW + timedelta(days=4)),                 # last day to list is in 2 days
                        _entry("X", NOW + timedelta(days=4), matched=0, new=True),   # not his product
                        _entry("Z", NOW + timedelta(days=1))])                # too late to list
    assert sorted(_kinds(rows)) == [("bid_list_product", "L"), ("bid_new", "N")]
