"""Step 3.3: OEM authorisation, OEM turnover and Q1/Q2 tags, for a reseller. Never blocks."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from gem_assistant.domain.models import (
    BidAnalysis, ClauseFlag, Evidence, ExtractedField, ExtractionMethod, FieldStatus, SellerProfile,
)
from gem_assistant.eligibility.rules import DEFAULT_RULES, OemRule, RestrictiveClauseRule

AT = datetime(2026, 10, 22, tzinfo=timezone.utc)
# Real form line from corpus bids 9930606 / 10036473, and the real item tag from 10017455.
DOCS = "Experience Criteria,Past Performance,Bidder Turnover,Certificate (Requested in ATC),OEM Authorization Certificate,OEM Annual Turnover"
ITEM = "Composite Office Tables conforming to IS 8126 (V2) (Q2)"


def _f(name, value, page=1):
    return ExtractedField(name=name, label=name, status=FieldStatus.FOUND, value=value,
                          evidence=Evidence(page=page, quote=value, method=ExtractionMethod.LABEL_PARSE))


def _bid(docs=None, item=None, flags=(), end="2026-11-02T17:00:00+05:30"):
    fields = [_f("bid_end", end)] + [_f(n, v, 2) for n, v in (("documents_required", docs), ("item_category", item)) if v]
    return BidAnalysis(bid_number="GEM/2026/B/1", source_name="x.pdf", sha256="a" * 64, page_count=1,
                       unread_lines=0, imported_at=AT, fields=fields, flags=list(flags))


def _run(bid, **profile):
    return OemRule().evaluate(bid, SellerProfile(**profile), AT)


def test_silent_when_nothing_asked_or_no_profile():
    assert _run(_bid(docs="Bidder Turnover,Experience Criteria")) == []
    assert OemRule().evaluate(_bid(docs=DOCS), None, AT) == []


def test_reseller_gets_one_merged_review_with_deadline():
    (r,) = _run(_bid(docs=DOCS))
    assert r.outcome.value == "NEEDS_REVIEW" and r.evidence.page == 2
    assert "OEM authorisation certificate" in r.reason and "turnover certificate" in r.reason
    assert "reseller" in r.reason and "Nov 2026" in r.reason


def test_the_maker_of_the_item_is_left_alone():
    bid = _bid(docs=DOCS, item=ITEM)
    assert _run(bid, is_oem=True) == []  # no oem_products listed: maker of everything
    assert _run(bid, is_oem=True, oem_products=["office tables"]) == []
    assert _run(bid, is_oem=True, oem_products=["printers"]) != []  # maker of something else
    assert _run(bid) != []  # is_oem false


def test_q2_tag_alone_asks_for_authorisation():
    (r,) = _run(_bid(item=ITEM))
    assert "(Q2)" in r.evidence.quote and "authorisation" in r.reason


def test_q1_tag_for_a_reseller_says_only_the_maker_can_offer():
    (r,) = _run(_bid(item="Some Item (V2) (Q1)"))
    assert "Q1" in r.reason and "only its maker" in r.reason and "GeM rule not confirmed" in r.reason


def test_authorisation_clause_flag_is_taken_over_from_restrictive_clauses():
    flag = ClauseFlag(category="oem_authorisation", label="OEM / authorisation requirement",
                      evidence=Evidence(page=4, quote="Bidder must submit OEM authorisation certificate.",
                                        method=ExtractionMethod.PATTERN_SCAN))
    bid = _bid(flags=[flag])
    (r,) = _run(bid)
    assert r.evidence.page == 4 and "OEM authorisation certificate" in r.reason
    assert RestrictiveClauseRule().evaluate(bid, None, AT) == []


def test_never_blocks_and_is_a_default_rule():
    assert all(r.outcome.value == "NEEDS_REVIEW" for r in _run(_bid(docs=DOCS, item="X (Q1)")))
    assert OemRule in {type(r) for r in DEFAULT_RULES}
