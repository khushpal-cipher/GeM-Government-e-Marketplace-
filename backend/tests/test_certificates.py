"""Step 3.3-prep: named standards (ISO / BIS / NABL / IS nnnn) the bid asks for vs his certificates."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from gem_assistant.domain.models import (
    BidAnalysis, ClauseFlag, Evidence, ExtractedField, ExtractionMethod, FieldStatus, SellerProfile,
)
from gem_assistant.eligibility.rules import CertificateRule, DEFAULT_RULES, standards_in

AT = datetime(2026, 10, 22, tzinfo=timezone.utc)
# Real sentence from corpus bids 9974983 and 9998303 (shortened after "approval certificates").
BIS = ("Certificates The bidder is required to upload, along with the bid, all relevant certificates such as "
       "BIS licence, type test certificate, approval certificates and test reports.")
ISO = "The bidder must hold a valid ISO 9001:2015 and ISO/IEC 27001 certificate and NABL accredited lab reports."


def _flag(text: str, page: int = 3) -> ClauseFlag:
    return ClauseFlag(category="certification", label="Certificate or test report needed",
                      evidence=Evidence(page=page, quote=text, method=ExtractionMethod.PATTERN_SCAN))


def _bid(flags=(), item: str | None = None) -> BidAnalysis:
    fields = [ExtractedField(name="item_category", label="Item", status=FieldStatus.FOUND, value=item,
                             evidence=Evidence(page=1, quote=item, method=ExtractionMethod.LABEL_PARSE))] if item else []
    return BidAnalysis(bid_number="GEM/2026/B/1", source_name="x.pdf", sha256="a" * 64, page_count=1,
                       unread_lines=0, imported_at=AT, fields=fields, flags=list(flags))


def _run(bid, certs, **kw):
    return CertificateRule().evaluate(bid, SellerProfile(certifications=certs, **kw), AT)


def test_standards_are_named_by_number_and_normalised():
    assert standards_in(ISO) == ["ISO 9001", "ISO 27001", "NABL"]
    assert standards_in(BIS) == ["BIS"]
    assert standards_in("iso  14001, is: 8126 and I S 8126") == ["ISO 14001", "IS 8126"]
    assert standards_in("ISO certified, ISI marked") == []


def test_silent_when_nothing_named_or_he_has_it():
    assert _run(_bid([_flag("Test reports are required.")]), []) == []
    assert _run(_bid([_flag(ISO)]), ["ISO 9001:2015", "ISO/IEC 27001", "NABL accredited"]) == []
    assert CertificateRule().evaluate(_bid([_flag(BIS)]), None, AT) == []


def test_empty_profile_list_gives_one_review_listing_all():
    (r,) = _run(_bid([_flag(ISO)]), [])
    assert r.outcome.value == "NEEDS_REVIEW"
    assert "ISO 9001, ISO 27001, NABL" in r.reason and "page 3" in r.reason and "Add your certificates" in r.reason


def test_one_review_per_missing_standard_and_iso_is_matched_by_number():
    results = _run(_bid([_flag(ISO)]), ["ISO 9001", "ISO"])  # a bare "ISO" does not cover ISO 27001
    assert [r.reason.split(" (")[0] for r in results] == ["The bid asks for ISO 27001", "The bid asks for NABL"]
    assert all("your profile lists ISO 9001, ISO" in r.reason for r in results)


def test_product_standard_in_item_name_matters_only_to_its_maker():
    bid = _bid(item="Office Chair, Composite Office Tables conforming to IS 8126 (V2)")
    assert _run(bid, ["ISO 9001"]) == []
    assert _run(bid, ["ISO 9001"], oem_products=["office tables"]) != []
    assert _run(bid, ["IS 8126"], oem_products=["office tables"]) == []


def test_never_blocks_and_is_a_default_rule():
    assert all(r.outcome.value != "BLOCKED" for r in _run(_bid([_flag(BIS)]), ["ISO 9001"]))
    assert CertificateRule in {type(r) for r in DEFAULT_RULES}
