"""Step 3.8: buyer terms GeM's own list says a buyer may not add. A review, never a block."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from gem_assistant.domain.models import BidAnalysis, ExtractedField, Evidence, ExtractionMethod, FieldStatus, PageText
from gem_assistant.eligibility.rules import DEFAULT_RULES, ForbiddenTermRule, RestrictiveClauseRule, SellerProfile
from gem_assistant.parsing.clause_scanner import PatternClauseScanner

AT = datetime(2026, 10, 22, 10, tzinfo=timezone.utc)


def _scan(text: str):
    page = PageText(number=9, text=f"/Buyer Added Bid Specific Terms and Conditions\n{text}\n/Disclaimer\n")
    return PatternClauseScanner().scan([page])


# Sentences written in the shape of GeM's list (items 2, 4, 7, 8, 10, 11). None of the 30 corpus bids has one.
@pytest.mark.parametrize("text, category", [
    ("Items of make Havells only shall be quoted.", "forbidden_brand"),
    ("Bidder must submit a hard copy of the technical bid in a sealed envelope before bid opening.", "forbidden_physical"),
    ("Sample must be submitted along with the bid.", "forbidden_sample"),
    ("Experience is valid only from Central Government department work.", "forbidden_experience"),
    ("Detailed terms and conditions are available on the website www.buyer-org.in.", "forbidden_external"),
    ("A tender fee of Rs 500 is payable.", "forbidden_fee"),
])
def test_each_listed_term_is_flagged(text, category):
    assert category in [f.category for f in _scan(text)]


@pytest.mark.parametrize("text", [
    # Real sentences from the corpus that must stay quiet.
    "Bidder has to upload scanned copy / proof of the DD along with bid and has to ensure delivery of hardcopy to the Buyer within 5 days of Bid End date.",
    "One manufacturer can also authorize only one agent/ dealer except for proprietary or standardized cases.",
    "Submission of invoice document in hard copy is allowed for invoices up to Rs five lakhs.",
    "Second Level: it may be escalated by lodging a formal grievance through the SUVIDHA Portal: https://suvidha.bhel.in/suvidha/.",
    "Send the EMD as a hard copy within 5 days.",
])
def test_ordinary_sentences_stay_quiet(text):
    assert not [f for f in _scan(text) if f.category.startswith("forbidden")]


def _bid(text: str, dated: str | None, end: str = "2026-11-12T17:00:00+05:30") -> BidAnalysis:
    f = lambda n, v: ExtractedField(name=n, label=n, status=FieldStatus.FOUND, value=v,
                                    evidence=Evidence(page=1, quote=v, method=ExtractionMethod.LABEL_PARSE))
    return BidAnalysis(bid_number="GEM/2026/B/1", source_name="x.pdf", sha256="a" * 64, page_count=1, unread_lines=0,
                       imported_at=AT, fields=[f("bid_end", end)] + ([f("bid_dated", dated)] if dated else []),
                       flags=_scan(text))


def _run(bid):
    return ForbiddenTermRule().evaluate(bid, SellerProfile(), AT)


def test_open_window_names_the_item_the_quote_and_the_last_day():
    (r,) = _run(_bid("A tender fee of Rs 500 is payable.", "2026-10-20"))  # 23 days open -> start + 4 = 24 Oct
    assert r.outcome.value == "NEEDS_REVIEW"
    assert "item 11" in r.reason and "A tender fee of Rs 500 is payable." in r.reason
    assert "24 Oct 2026" in r.reason and "Only one representation per bid" in r.reason


@pytest.mark.parametrize("dated, end, last_day", [
    ("2026-10-20", "2026-10-28T17:00:00+05:30", "by today"),  # 8 days -> +2 = 22 Oct
    ("2026-10-22", "2026-10-26T17:00:00+05:30", "by tomorrow"),  # 4 days -> +1 = 23 Oct
])
def test_window_length_depends_on_days_open(dated, end, last_day):
    (r,) = _run(_bid("A tender fee of Rs 500 is payable.", dated, end))
    assert last_day in r.reason


def test_window_passed_and_date_unknown():
    (r,) = _run(_bid("A tender fee of Rs 500 is payable.", "2026-10-01"))
    assert "has passed" in r.reason and "skip" in r.reason
    (r,) = _run(_bid("A tender fee of Rs 500 is payable.", None))
    assert "date unknown; check on GeM" in r.reason


def test_silent_without_flags_never_blocks_and_not_double_listed():
    assert _run(_bid("Delivery within 30 days.", "2026-10-20")) == []
    bid = _bid("A tender fee of Rs 500 is payable.", "2026-10-20")
    assert RestrictiveClauseRule().evaluate(bid, None, AT) == []
    assert ForbiddenTermRule in {type(r) for r in DEFAULT_RULES}
