"""Step 3.7: PAC (Proprietary Article Certificate) bids name one make. Never blocks."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from gem_assistant.domain.models import BidAnalysis, ClauseFlag, Evidence, ExtractionMethod, PageText, SellerProfile
from gem_assistant.eligibility.rules import DEFAULT_RULES, PacRule
from gem_assistant.infrastructure.pypdf_extractor import PypdfTextExtractor
from gem_assistant.parsing.clause_scanner import PatternClauseScanner
from gem_assistant.parsing.label_extractor import LabelFieldExtractor

AT = datetime(2026, 10, 22, tzinfo=timezone.utc)
FIX = Path(__file__).parent / "fixtures"


def _analyse(name: str) -> BidAnalysis:
    pages = PypdfTextExtractor(300).extract((FIX / name).read_bytes())
    return BidAnalysis(bid_number="GEM/2026/B/1", source_name=name, sha256="a" * 64, page_count=len(pages),
                       unread_lines=0, imported_at=AT, fields=LabelFieldExtractor().extract(pages),
                       flags=PatternClauseScanner().scan(pages))


def test_the_real_pac_bid_is_reviewed_with_its_quote():
    results = PacRule().evaluate(_analyse("GEM-bid-9781965_pac.pdf"), SellerProfile(), AT)
    assert results and all(r.outcome.value == "NEEDS_REVIEW" for r in results)
    text = " ".join(r.reason for r in results)
    assert "PAC bid" in text and "PAC Bidding" in text and "maker's authorisation" in text
    assert {r.evidence.page for r in results} >= {3, 46}  # the bid form's MII-waiver line and the ATC line


def test_gems_standard_sentence_about_pac_buying_is_not_a_pac_bid():
    standard = ("Mandating procurement of / from specific Brand / Make / Model / Manufacturer / Dealer except in "
                "case of Single Bid / Proprietary Article Certificate (PAC) Buying. Then such PAC may not be required.")
    page = PageText(number=7, text=f"/Buyer Added Bid Specific Terms and Conditions\n{standard}\n/Disclaimer\n")
    assert PatternClauseScanner().scan([page]) == []


def test_ordinary_bid_is_silent_and_pac_is_a_default_rule():
    assert PacRule().evaluate(_analyse("GEM-2026-B-8105558_doc9971825.pdf"), SellerProfile(), AT) == []
    assert PacRule in {type(r) for r in DEFAULT_RULES}
