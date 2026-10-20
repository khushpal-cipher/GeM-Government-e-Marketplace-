"""Step 1.3: shortfall-reply helper.

From a pasted clarification, lists each document asked (OEM turnover, OEM authorisation,
past performance, GST, ITR, Udyam, etc.), checks which the seller's profile says he has,
and drafts the covering note following 1.0 wording rules.
"""

from __future__ import annotations

from datetime import date, datetime, timezone

import pytest
from fastapi.testclient import TestClient

from gem_assistant.api.app import create_app
from gem_assistant.domain.models import SellerProfile
from gem_assistant.domain.shortfall import (
    RequestedDocument,
    ShortfallReply,
    detect_documents,
    draft_covering_note,
    shortfall_reply,
)
from gem_assistant.domain.wording import DRAFT_NOTE, check_draft

NOW = datetime(2026, 10, 20, 6, 30, tzinfo=timezone.utc)  # Tue 20 Oct 2026, 12:00 PM IST

SAMPLE_CLARIFICATION = """Clarification History
Bid No: GEM/2026/B/6123456
Request no 4411, General clarification, last date to respond 24-10-2026
Please submit OEM turnover for last 3 years and OEM authorisation.
Status: Pending"""


def test_detects_oem_turnover_and_authorisation():
    docs = detect_documents("Please submit OEM turnover for last 3 years and OEM authorisation.")
    names = [d.name for d in docs]
    assert "OEM Turnover" in names
    assert "OEM Authorisation" in names
    for d in docs:
        assert d.quote in "Please submit OEM turnover for last 3 years and OEM authorisation."
        assert d.placeholder.startswith("[attach:")


def test_detects_gst_itr_and_udyam_certificates():
    text = "Submit GST certificate, last 3 years ITR acknowledgement, and Udyam registration certificate."
    docs = detect_documents(text)
    names = [d.name for d in docs]
    assert "GST Certificate" in names
    assert "Income Tax Returns (ITR)" in names
    assert "MSE / Udyam Certificate" in names


def test_detects_iso_and_bis_certifications():
    text = "Required: ISO 9001 certificate and BIS certification copy."
    docs = detect_documents(text)
    names = [d.name for d in docs]
    assert any("ISO" in n for n in names)
    assert any("BIS" in n for n in names)


def test_detects_experience_and_turnover_and_undertakings():
    text = ("Kindly upload past performance certificate, CA certified annual turnover, "
            "and Make in India (MII) declaration.")
    docs = detect_documents(text)
    names = [d.name for d in docs]
    assert "Past Performance / Experience" in names
    assert "Bidder Annual Turnover" in names
    assert any("Declaration" in n or "Undertaking" in n for n in names)


def test_fallback_when_unmatched_document_is_asked():
    text = "Please furnish laboratory test report from NABL accredited lab."
    docs = detect_documents(text)
    assert len(docs) >= 1
    assert any("laboratory test report" in d.quote.lower() or "test report" in d.name.lower() for d in docs)


def test_profile_matching_for_reseller_vs_oem():
    text = "Please submit OEM authorisation."
    reseller_profile = SellerProfile(is_oem=False, oem_products=[])
    reply_reseller = shortfall_reply(text, reseller_profile, now=NOW)
    doc_reseller = reply_reseller.documents[0]
    assert doc_reseller.in_profile is False
    assert "reseller" in doc_reseller.profile_note.lower()

    oem_profile = SellerProfile(is_oem=True)
    reply_oem = shortfall_reply(text, oem_profile, now=NOW)
    doc_oem = reply_oem.documents[0]
    assert doc_oem.in_profile is True
    assert "oem" in doc_oem.profile_note.lower()


def test_profile_matching_for_mse_and_certifications():
    text = "Provide Udyam certificate and ISO 9001 certificate."
    profile_with_docs = SellerProfile(
        is_mse=True, certifications=["ISO 9001:2015", "CE"])
    reply = shortfall_reply(text, profile_with_docs, now=NOW)
    by_name = {d.name: d for d in reply.documents}
    assert by_name["MSE / Udyam Certificate"].in_profile is True
    assert any(d.in_profile is True for name, d in by_name.items() if "ISO" in name)

    profile_without_docs = SellerProfile(is_mse=False, certifications=[])
    reply_empty = shortfall_reply(text, profile_without_docs, now=NOW)
    by_name_empty = {d.name: d for d in reply_empty.documents}
    assert by_name_empty["MSE / Udyam Certificate"].in_profile is False
    assert any(d.in_profile is False for name, d in by_name_empty.items() if "ISO" in name)


def test_profile_matching_for_turnover_and_experience():
    text = "Submit bidder turnover for last 3 years and past experience documents."
    profile = SellerProfile(annual_turnover_rupees=5000000, years_experience=4)
    reply = shortfall_reply(text, profile, now=NOW)
    for d in reply.documents:
        assert d.in_profile is True


def test_draft_follows_wording_rules_and_passes_check_draft():
    profile = SellerProfile(business_name="Apex Traders")
    reply = shortfall_reply(SAMPLE_CLARIFICATION, profile, now=NOW)

    assert reply.bid_number == "GEM/2026/B/6123456"
    assert reply.due == date(2026, 10, 24)
    assert reply.due_text == "by Sat 24 Oct 2026 (4 days left)"

    draft = reply.draft
    assert draft.startswith(DRAFT_NOTE)
    assert "GEM/2026/B/6123456" in draft
    assert "Apex Traders" in draft
    assert "[attach: OEM authorisation]" in draft or "[attach: OEM" in draft
    # Quotes the buyer's clarification text
    assert "Please submit OEM turnover for last 3 years and OEM authorisation." in draft

    # Crucial: 1.0 wording rules validation
    problems = check_draft(draft)
    assert problems == [], f"Draft violates wording rules: {problems}"


def test_draft_without_bid_number_or_business_name_uses_placeholders():
    reply = shortfall_reply("Please provide GST registration certificate.", SellerProfile(), now=NOW)
    assert reply.bid_number is None
    assert "[your firm name]" in reply.draft
    assert "[bid number]" in reply.draft
    assert check_draft(reply.draft) == []


@pytest.fixture
def client(container):
    return TestClient(create_app(container, allowed_hosts=frozenset({"testserver"})))


def test_api_endpoint_shortfall_reply(client):
    response = client.post("/api/shortfall/reply", json={
        "text": SAMPLE_CLARIFICATION
    })
    assert response.status_code == 200
    data = response.json()
    assert data["bid_number"] == "GEM/2026/B/6123456"
    assert data["due"] == "2026-10-24"
    assert len(data["documents"]) == 2
    assert data["draft"].startswith(DRAFT_NOTE)
    assert check_draft(data["draft"]) == []
