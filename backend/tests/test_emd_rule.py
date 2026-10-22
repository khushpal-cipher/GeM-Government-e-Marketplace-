"""Step 3.4: EMD. The page-break fix on a real bid, then the rule's cases. Never blocks."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from gem_assistant.domain.models import (
    BidAnalysis, ClauseFlag, Evidence, ExtractedField, ExtractionMethod, FieldStatus, SellerProfile,
)
from gem_assistant.eligibility.rules import EmdRule
from gem_assistant.infrastructure.pypdf_extractor import PypdfTextExtractor
from gem_assistant.parsing.clause_scanner import PatternClauseScanner
from gem_assistant.parsing.label_extractor import LabelFieldExtractor

AT = datetime(2026, 10, 22, tzinfo=timezone.utc)
PDF = Path(__file__).parent / "fixtures" / "GEM-bid-9748067_emd-over-page-break.pdf"


def test_emd_split_over_a_page_break_is_still_found():
    # Real bid 9748067: "/EMD Detail /Advisory Bank <bank>" ends page 2, "/EMD Amount 34000" starts page 3.
    fields = {f.name: f for f in LabelFieldExtractor().extract(PypdfTextExtractor(300).extract(PDF.read_bytes()))}
    assert (fields["emd_required"].status, fields["emd_required"].value) == (FieldStatus.FOUND, "Yes")
    assert fields["emd_required"].evidence.page == 2
    assert fields["emd_amount"].value == "34000"


def _f(name, value, page=2):
    return ExtractedField(name=name, label=name, status=FieldStatus.FOUND, value=value,
                          evidence=Evidence(page=page, quote=f"{name} {value}", method=ExtractionMethod.LABEL_PARSE))


def _bid(emd="Yes", amount="34000", value=None, item="Office Chair", flags=()):
    fields = [_f("bid_end", "2026-11-02T17:00:00+05:30")]
    fields += [_f("emd_required", emd)] if emd else []
    fields += [_f("emd_amount", amount)] if amount else []
    fields += [_f("estimated_bid_value", value)] if value else []
    fields += [_f("item_category", item)] if item else []
    return BidAnalysis(bid_number="GEM/2026/B/1", source_name="x.pdf", sha256="a" * 64, page_count=1,
                       unread_lines=0, imported_at=AT, fields=fields, flags=list(flags))


def _run(bid, **profile):
    return EmdRule().evaluate(bid, SellerProfile(**profile), AT)


def test_no_emd_is_silent():
    assert _run(_bid(emd="No", amount=None)) == []
    assert _run(_bid(emd=None, amount=None)) == []


def test_an_amount_without_the_required_flag_still_counts_as_asked():
    (r,) = _run(_bid(emd=None))
    assert "₹34,000" in r.reason


def test_not_exempt_pays_before_the_deadline():
    (r,) = _run(_bid())
    assert r.outcome.value == "NEEDS_REVIEW" and "Pay an EMD of ₹34,000 before the bid closes" in r.reason
    assert "Nov 2026" in r.reason


def test_estimated_value_below_five_lakh_points_to_gtc():
    (r,) = _run(_bid(value="450000"))
    assert "below ₹5 lakh" in r.reason and "₹4,50,000" in r.reason and "representation" in r.reason
    assert _run(_bid(value="500000"))[0].reason.startswith("Pay an EMD")


@pytest.mark.parametrize("profile, words", [
    (dict(is_mse=True, own_made_products=["office chair"]), "you may be exempt (MSE making this item"),
    (dict(is_startup=True), "DPIIT startup"),
    (dict(is_mse=True), "add the items you make to your profile"),
    (dict(is_mse=True, own_made_products=["printers"]), "covers only items you make, so pay it before"),
])
def test_msme_and_startup_cases(profile, words):
    (r,) = _run(_bid(), **profile)
    assert r.outcome.value == "NEEDS_REVIEW" and words in r.reason and "₹34,000" in r.reason


def test_state_limit_clause_quote_is_added_to_the_exemption():
    text = "EMD exemption for MSE is available only to sellers of the state of the buyer."
    from gem_assistant.domain.models import PageText
    pages = [PageText(number=3, text=f"/Buyer Added Bid Specific Terms and Conditions\n{text}\n/Disclaimer\n")]
    flags = PatternClauseScanner().scan(pages)
    assert "emd_state_limit" in [f.category for f in flags]
    (r,) = _run(_bid(flags=flags), is_mse=True, own_made_products=["office chair"])
    assert text in r.reason
