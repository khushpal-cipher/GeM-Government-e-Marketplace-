"""Step 1.5: Rejection reason reader + challenge draft (progress.md step 1.5).

When the seller pastes the buyer's disqualification reason from GeM (Bids -> List of Bids ->
Already participated -> View Result / Technical Evaluation), the app:
1. Identifies the missing document or technical ground.
2. Checks it against the seller's profile (1.1).
3. Computes the 48-hour one-time challenge deadline.
4. Drafts the one-time challenge following 1.0 wording rules (DRAFT_NOTE, quotes buyer, placeholders).
5. Remembers past rejections in SQLite so future checklists warn earlier.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
import pytest
from fastapi.testclient import TestClient

from gem_assistant.api.app import create_app
from gem_assistant.domain.models import SellerProfile
from gem_assistant.domain.rejection import (
    DisqualificationAnalysis,
    MissingDoc,
    analyze_rejection,
    check_rejection_warnings,
    draft_challenge,
)
from gem_assistant.domain.wording import DRAFT_NOTE, check_draft

NOW = datetime(2026, 10, 20, 10, 0, tzinfo=timezone.utc)  # Tue 20 Oct 2026, 3:30 PM IST


def test_detects_missing_oem_authorisation():
    text = "Disqualified: Non-submission of OEM Authorisation Certificate as per ATC clause 4."
    analysis = analyze_rejection(text, now=NOW)
    assert any("OEM Authorisation" in d.name for d in analysis.missing_docs)
    assert any("OEM Authorisation" in d.quote for d in analysis.missing_docs)
    assert analysis.primary_reason == "OEM Authorisation"


def test_detects_mse_udyam_missing_for_emd():
    text = "Technical evaluation rejected: MSE / Udyam certificate not uploaded. EMD exemption not admissible."
    analysis = analyze_rejection(text, now=NOW)
    names = [d.name for d in analysis.missing_docs]
    assert "MSE / Udyam Certificate" in names
    assert analysis.emd_involved is True


def test_detects_turnover_and_experience_rejections():
    text = ("Bidder disqualified in technical evaluation: Average annual turnover criteria of ₹50 Lakh "
            "not met and past experience certificates of 3 years not furnished.")
    analysis = analyze_rejection(text, now=NOW)
    names = [d.name for d in analysis.missing_docs]
    assert "Bidder Annual Turnover" in names
    assert "Past Performance / Experience" in names


def test_detects_technical_spec_deviation():
    text = "Rejected in technical evaluation: Technical specification deviation - offered CPU speed 2.4 GHz does not meet minimum 3.0 GHz required."
    analysis = analyze_rejection(text, now=NOW)
    assert analysis.technical_deviation is True
    assert "technical specification deviation" in analysis.summary.lower()


def test_detects_make_in_india_and_undertakings():
    text = "Disqualified: Local Content declaration (Make in India) and Land Border declaration not submitted."
    analysis = analyze_rejection(text, now=NOW)
    names = [d.name for d in analysis.missing_docs]
    assert any("Make in India" in n or "Declaration" in n for n in names)


def test_extracts_bid_number_and_eval_date():
    text = """Bid No: GEM/2026/B/8765432
Date of Technical Evaluation: 20-10-2026
Reason for Disqualification: OEM turnover certificate for last 3 years not uploaded."""
    analysis = analyze_rejection(text, now=NOW)
    assert analysis.bid_number == "GEM/2026/B/8765432"
    assert analysis.evaluation_date == date(2026, 10, 20)
    assert analysis.challenge_deadline_date == date(2026, 10, 22)  # +48 hours / 2 days


def test_48_hour_challenge_deadline_calculation():
    eval_date = date(2026, 10, 20)
    analysis = analyze_rejection(
        "Disqualified due to missing GST certificate",
        bid_number="GEM/2026/B/1112223",
        eval_date=eval_date,
        now=NOW,
    )
    assert analysis.challenge_deadline_date == date(2026, 10, 22)
    assert "48 hours" in analysis.deadline_text
    assert "Thu 22 Oct 2026" in analysis.deadline_text


def test_profile_rebuttal_for_mse_seller():
    text = "Disqualified: EMD not paid and MSE certificate not furnished."
    profile = SellerProfile(is_mse=True)
    analysis = analyze_rejection(text, profile=profile, now=NOW)
    assert analysis.has_rebuttal is True
    assert any("registered micro/small enterprise" in r.lower() or "udyam" in r.lower() for r in analysis.rebuttal_points)


def test_profile_rebuttal_for_oem_seller():
    text = "Disqualified: OEM Authorisation not submitted."
    profile = SellerProfile(is_oem=True)
    analysis = analyze_rejection(text, profile=profile, now=NOW)
    assert analysis.has_rebuttal is True
    assert any("original equipment manufacturer" in r.lower() or "oem self-declaration" in r.lower() for r in analysis.rebuttal_points)


def test_profile_rebuttal_for_turnover_and_experience():
    text = "Disqualified: Bidder turnover certificate and past experience not provided."
    profile = SellerProfile(annual_turnover_rupees=7500000, years_experience=4)
    analysis = analyze_rejection(text, profile=profile, now=NOW)
    assert any("7,500,000" in r for r in analysis.rebuttal_points)
    assert any("4 years" in r for r in analysis.rebuttal_points)


def test_challenge_draft_adheres_to_1_0_wording_rules():
    text = "Disqualified: Non-submission of OEM Authorisation Certificate."
    profile = SellerProfile(is_oem=True)
    analysis = analyze_rejection(text, bid_number="GEM/2026/B/8765432", eval_date=date(2026, 10, 20), profile=profile, now=NOW)

    draft = analysis.challenge_draft
    assert draft.startswith(DRAFT_NOTE)
    problems = check_draft(draft)
    assert problems == [], f"Draft violates wording rules: {problems}"

    # Contains required context & GeM rule
    assert "GEM/2026/B/8765432" in draft
    assert "one-time" in draft.lower() or "representation" in draft.lower()
    assert "48 hours" in draft
    assert "[attach:" in draft
    assert "[Your Name" in draft or "[Authorized Signatory" in draft


def test_rejection_repository_and_warning(tmp_path):
    from gem_assistant.infrastructure.database import Database
    from gem_assistant.infrastructure.sqlite_repositories import SqliteRejectionRepository

    db = Database(tmp_path / "test.db")
    db.migrate()
    repo = SqliteRejectionRepository(db)

    # Save a rejection
    rec_id = repo.save_rejection(
        bid_number="GEM/2026/B/9998887",
        reason_text="OEM Authorisation certificate not submitted",
        missing_doc="OEM Authorisation",
        category="authorisation",
    )
    assert rec_id > 0

    # Retrieve history
    history = repo.list_rejections()
    assert len(history) == 1
    assert history[0]["bid_number"] == "GEM/2026/B/9998887"
    assert history[0]["missing_doc"] == "OEM Authorisation"

    # Warning on checklist documents
    warnings = repo.find_warnings_for_docs(["OEM Authorisation", "GST Certificate"])
    assert len(warnings) == 1
    assert "GEM/2026/B/9998887" in warnings[0]["bid_number"]
    assert warnings[0]["missing_doc"] == "OEM Authorisation"

    # Delete
    assert repo.delete_rejection(rec_id) is True
    assert len(repo.list_rejections()) == 0


def test_rejection_api_routes(container):
    app = create_app(container, allowed_hosts=frozenset({"testserver"}))
    client = TestClient(app)

    # 1. Analyze
    res = client.post("/api/rejection/analyze", json={
        "text": "Bid GEM/2026/B/5554443 disqualified: Udyam certificate not provided.",
        "eval_date": "2026-10-20"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["bid_number"] == "GEM/2026/B/5554443"
    assert any("Udyam" in d["name"] for d in data["missing_docs"])
    assert data["challenge_draft"].startswith(DRAFT_NOTE)

    # 2. Save to history
    save_res = client.post("/api/rejection/history", json={
        "bid_number": data["bid_number"],
        "reason_text": "Udyam certificate not provided",
        "missing_doc": "MSE / Udyam Certificate",
        "category": "registration",
    })
    assert save_res.status_code == 200
    rec_id = save_res.json()["id"]

    # 3. Get history
    hist_res = client.get("/api/rejection/history")
    assert hist_res.status_code == 200
    items = hist_res.json()["items"]
    assert len(items) >= 1
    assert items[0]["bid_number"] == "GEM/2026/B/5554443"

    # 4. Check warnings for future checklist
    warn_res = client.get("/api/rejection/warnings?docs=MSE%20/%20Udyam%20Certificate,ISO")
    assert warn_res.status_code == 200
    warns = warn_res.json()["warnings"]
    assert len(warns) == 1
    assert warns[0]["missing_doc"] == "MSE / Udyam Certificate"

    # 5. Delete from history
    del_res = client.delete(f"/api/rejection/history/{rec_id}")
    assert del_res.status_code == 200
    assert client.get("/api/rejection/history").json()["items"] == []
