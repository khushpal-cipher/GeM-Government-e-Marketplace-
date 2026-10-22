"""Step 2.4: per-bid document checklist."""

from __future__ import annotations

from gem_assistant.domain.checklist import UnreadFile, build_checklist
from gem_assistant.domain.models import PageText, SellerProfile

from .conftest import FIXTURES

FORM = "Experience Criteria,Past Performance,Bidder Turnover,Certificate (Requested in ATC),Additional Doc 1 (Requested in ATC)"


def test_form_list_becomes_documents_atc_slots_and_dedupes():
    result = build_checklist(FORM, 2, [], [], SellerProfile(annual_turnover_rupees=5_000_000))
    names = [i.name for i in result.items]
    assert names == ["Past Performance / Experience", "Bidder Annual Turnover", "Certificate", "Additional Doc 1"]
    assert [i.from_atc_slot for i in result.items] == [False, False, True, True]
    assert result.items[1].in_profile is True and all(i.page == 2 for i in result.items)
    assert "10 MB" in result.upload_rules


def test_attached_file_text_adds_documents_and_unread_files_are_listed():
    spec = [PageText(number=3, text="Bidder must submit ISO 9001 certificate.")]
    unread = [UnreadFile("atc", "https://x", "This file is a scan; open it yourself.")]
    result = build_checklist(None, None, [("atc", spec)], unread, None)
    assert [(i.source, i.page) for i in result.items] == [("atc", 3)] and "ISO 9001" in result.items[0].name
    assert result.unread_files == unread


def test_a_past_rejection_for_the_same_document_warns():
    warn = lambda names: [{"missing_doc": "Bidder Annual Turnover", "warning": "Rejected before"}]
    result = build_checklist("Bidder Turnover", 1, [], [], None, warn)
    assert result.items[0].past_rejection == "Rejected before"


def test_every_entry_of_a_real_bid_form_list_is_in_its_quote():
    from gem_assistant.infrastructure.pypdf_extractor import PypdfTextExtractor
    from gem_assistant.parsing.label_extractor import LabelFieldExtractor
    from gem_assistant.domain.checklist import form_entries

    pdf = (FIXTURES / "GEM-2026-B-8105558_doc9971825.pdf").read_bytes()
    field = next(f for f in LabelFieldExtractor().extract(PypdfTextExtractor(300).extract(pdf))
                 if f.name == "documents_required")
    quote = " ".join(field.evidence.quote.split())
    assert len(form_entries(field.value)) == 2 and all(e in quote for e in form_entries(field.value))
