"""Step 7.1: draft question to the buyer about forbidden terms (sentences written in the shape of GeM's list)."""

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from gem_assistant.domain.models import ClauseFlag, Evidence, ExtractionMethod
from gem_assistant.domain.wording import DRAFT_NOTE, check_draft
from gem_assistant.services.representation_service import RepresentationService

IST = timezone(timedelta(hours=5, minutes=30))
NOW = datetime(2026, 10, 23, 10, tzinfo=IST)


def _flag(category, quote, page=9):
    return ClauseFlag(category=category, label="x", evidence=Evidence(page=page, quote=quote, method=ExtractionMethod.PATTERN_SCAN))


def _service(flags, dated="2026-10-21", business="Sharma Traders"):
    bid = SimpleNamespace(bid_number="GEM/2026/B/1234567", flags=flags,
                          found_value=lambda name: dated if name == "bid_dated" else None,
                          deadline=lambda: datetime(2026, 11, 5, 15, tzinfo=IST))
    bids = SimpleNamespace(get=lambda i: SimpleNamespace(bid=bid) if i == 1 else None)
    profiles = SimpleNamespace(get=lambda: SimpleNamespace(business_name=business))
    return RepresentationService(bids, profiles, SimpleNamespace(now=lambda: NOW))


def test_draft_quotes_each_term_with_page_and_gem_list_item():
    result = _service([_flag("forbidden_brand", "Items of make Havells only shall be quoted."),
                       _flag("forbidden_fee", "A tender fee of Rs 500 is payable.", page=11)]).draft(1)
    text = result["draft"]
    assert text.startswith(DRAFT_NOTE)
    assert "page 9: “Items of make Havells only shall be quoted.”" in text
    assert "page 11: “A tender fee of Rs 500 is payable.”" in text
    assert "item 2:" in text and "item 11:" in text and text.rstrip().endswith("Sharma Traders")
    assert result["problems"] == [] and check_draft(text) == []


def test_last_date_is_a_dated_deadline():
    # bid dated 21 Oct, closes 5 Nov (15 days open): 4 days -> end of Sun 25 Oct 2026
    assert "25 Oct 2026" in _service([_flag("forbidden_fee", "A tender fee of Rs 500 is payable.")]).draft(1)["last_date"]


def test_unknown_firm_and_date_use_placeholders_not_guesses():
    result = _service([_flag("forbidden_fee", "A tender fee of Rs 500 is payable.")], dated=None, business="").draft(1)
    assert result["draft"].rstrip().endswith("[your firm name]") and "unknown" in result["last_date"]


def test_no_forbidden_term_no_draft_and_unknown_bid_is_none():
    svc = _service([_flag("restrictive_x", "Something else.")])
    assert svc.draft(1)["draft"] is None and svc.draft(2) is None
