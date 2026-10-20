"""Step 1.5: Rejection reason reader + challenge draft (progress.md step 1.5).

When the seller pastes the buyer's disqualification reason from GeM (Bids -> List of Bids ->
Already participated -> View Result / Technical Evaluation), this domain module:
1. Identifies missing documents or technical grounds using deterministic patterns.
2. Checks them against the seller's profile (1.1).
3. Computes the strict 48-hour one-time challenge window under GeM rules.
4. Generates a formal challenge / representation draft complying with 1.0 wording rules (DRAFT_NOTE).
5. Provides helper functions to check past rejections so future checklists warn earlier.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from typing import Sequence

from .gem_alerts import _DATE, _REF, MONTHS
from .models import SellerProfile
from .shortfall import _DOC_PATTERNS, _check_profile_for_doc
from .wording import DRAFT_NOTE, IST, check_draft, deadline


@dataclass(frozen=True)
class MissingDoc:
    name: str
    quote: str
    in_profile: bool | None
    profile_note: str
    placeholder: str


@dataclass(frozen=True)
class DisqualificationAnalysis:
    bid_number: str | None
    raw_text: str
    evaluation_date: date | None
    challenge_deadline_date: date | None
    deadline_text: str
    missing_docs: list[MissingDoc]
    primary_reason: str
    summary: str
    emd_involved: bool
    technical_deviation: bool
    has_rebuttal: bool
    rebuttal_points: list[str]
    challenge_draft: str


_TECHNICAL_SPEC_PATTERNS = [
    re.compile(r"\b(?:technical\s+specification\s+deviation|specification\s+deviation|spec\s+deviation)\b", re.IGNORECASE),
    re.compile(r"\b(?:not\s+meeting\s+(?:the\s+)?spec(?:ification)?|deviation\s+in\s+spec(?:ification)?|spec(?:ification)?\s+mismatch)\b", re.IGNORECASE),
    re.compile(r"\b(?:technical\s+non[- ]compliance|technically\s+non[- ]compliant)\b", re.IGNORECASE),
    re.compile(r"\b(?:parameter\s+not\s+met|criteria\s+not\s+met|does\s+not\s+meet\s+(?:minimum|required))\b", re.IGNORECASE),
]

_EMD_PATTERNS = [
    re.compile(r"\b(?:emd|earnest\s+money\s+deposit|bid\s+security)\b", re.IGNORECASE),
]

_DISQUALIFIED_PREFIX = re.compile(
    r"\b(?:disqualified(?:\s+due\s+to|\s+in|\s+reason)?|rejected(?:\s+in|\s+due\s+to)?|technical\s+evaluation\s+rejected|disqualification\s+reason)\b\s*[:\-]?\s*",
    re.IGNORECASE,
)


def _extract_eval_date(text: str) -> date | None:
    for m in _DATE.finditer(text):
        try:
            if m.group("y2"):
                return date(int(m.group("y2")), int(m.group("m2")), int(m.group("d2")))
            month = int(m.group("m")) if m.group("m") else MONTHS.get(m.group("mon").lower())
            if month:
                return date(int(m.group("y")), month, int(m.group("d")))
        except ValueError:
            continue
    return None


def _detect_rejection_documents(text: str, profile: SellerProfile | None) -> list[MissingDoc]:
    docs: list[MissingDoc] = []
    seen_names: set[str] = set()

    # Reuse and check standard patterns from shortfall
    for pattern, name, placeholder in _DOC_PATTERNS:
        match = pattern.search(text)
        if match and name not in seen_names:
            seen_names.add(name)
            quote = match.group(0).strip()
            in_prof, note = _check_profile_for_doc(name, quote, profile) if profile else (None, "No profile loaded.")
            docs.append(MissingDoc(name=name, quote=quote, in_profile=in_prof, profile_note=note, placeholder=placeholder))

    # Additional patterns specific to technical evaluation rejections
    # EMD exemption / MSE certificate
    if re.search(r"\b(?:emd\s+exemption|earnest\s+money)\b", text, re.IGNORECASE):
        if "MSE / Udyam Certificate" not in seen_names and re.search(r"\b(?:mse|udyam|msme)\b", text, re.IGNORECASE):
            seen_names.add("MSE / Udyam Certificate")
            in_prof = profile.is_mse if profile else None
            note = "Profile says MSE is Yes (EMD exemption applicable)" if in_prof else "EMD exemption claimed without valid MSE certificate"
            docs.append(MissingDoc(
                name="MSE / Udyam Certificate",
                quote="MSE / Udyam certificate for EMD exemption",
                in_profile=in_prof,
                profile_note=note,
                placeholder="[attach: Udyam Registration Certificate for EMD exemption]",
            ))

    # Make in India (Local Content)
    if re.search(r"\b(?:local\s+content|make\s+in\s+india|mii)\b", text, re.IGNORECASE):
        if not any("Make in India" in d.name for d in docs):
            docs.append(MissingDoc(
                name="Make in India (Local Content) Declaration",
                quote=re.search(r"\b(?:local\s+content|make\s+in\s+india|mii)\b[^\.\,\;\n]*", text, re.IGNORECASE).group(0),
                in_profile=True if profile and profile.is_oem else None,
                profile_note="Self-declaration of local content percentage as per MII order",
                placeholder="[attach: Make in India local content declaration certificate]",
            ))

    return docs


def draft_challenge(
    bid_number: str | None,
    evaluation_date: date | None,
    buyer_reason: str,
    rebuttal_points: Sequence[str],
    missing_docs: Sequence[MissingDoc],
) -> str:
    """Drafts a formal one-time challenge representation within the 48-hour GeM window."""
    lines: list[str] = [
        DRAFT_NOTE,
        "",
        "To,",
        "The Competent Authority / Buyer Officer,",
        f"Subject: Representation / Challenge against Technical Evaluation Rejection for Bid {bid_number or '[Bid Number]'}",
        "",
        "Respected Sir/Madam,",
        "",
        f"With reference to the technical evaluation results published for Bid No. {bid_number or '[Bid Number]'}"
        + (f" on {evaluation_date.strftime('%d-%m-%Y')}" if evaluation_date else "")
        + f", we submit this representation within the 48-hour one-time challenge window provided under GeM General Terms and Conditions (GTC).",
        "",
        "1. REASON STATED FOR DISQUALIFICATION:",
        f'"{buyer_reason.strip()}"',
        "",
        "2. FACTUAL REBUTTAL & SUBMISSION:",
    ]

    if rebuttal_points:
        for idx, pt in enumerate(rebuttal_points, start=1):
            lines.append(f"  2.{idx} {pt}")
    else:
        lines.append("  2.1 We have complied with all mandatory criteria stipulated in the Bid document and ATC.")

    lines.extend([
        "",
        "3. ENCLOSED SUPPORTING DOCUMENTS:",
    ])

    if missing_docs:
        for doc in missing_docs:
            lines.append(f"  - {doc.placeholder} (in reference to {doc.name})")
    else:
        lines.append("  - [attach: relevant supporting certificates and compliance documents]")

    lines.extend([
        "",
        "In light of the documentary evidence provided herewith, we respectfully request you to kindly review and reconsider our technical evaluation status.",
        "",
        "Important: Under GeM rules, this representation can only be submitted once within 48 hours of technical evaluation. Ensure all supporting documents are attached before clicking submit on GeM.",
        "",
        "Thanking you,",
        "Yours faithfully,",
        "[Your Name / Authorized Signatory]",
        "[Company / Firm Name]",
    ])

    return "\n".join(lines)


def analyze_rejection(
    text: str,
    bid_number: str | None = None,
    eval_date: date | None = None,
    profile: SellerProfile | None = None,
    now: datetime | None = None,
) -> DisqualificationAnalysis:
    now = now or datetime.now(timezone.utc)
    text_clean = text.strip()

    # 1. Bid number
    if not bid_number:
        ref_match = _REF.search(text_clean)
        if ref_match:
            bid_number = ref_match.group(0).upper()

    # 2. Evaluation Date & 48-hour Challenge Deadline
    if not eval_date:
        eval_date = _extract_eval_date(text_clean)

    if eval_date:
        deadline_date = eval_date + timedelta(days=2)  # 48 hours = 2 days
        deadline_dt = datetime(deadline_date.year, deadline_date.month, deadline_date.day, 23, 59, tzinfo=IST)
        deadline_str = f"within 48 hours ({deadline(deadline_date, now)})"
    else:
        deadline_date = None
        deadline_str = "within 48 hours of technical evaluation results publication on GeM"

    # 3. Detect Documents
    missing_docs = _detect_rejection_documents(text_clean, profile)

    # 4. Check Technical spec deviation
    technical_dev = any(p.search(text_clean) for p in _TECHNICAL_SPEC_PATTERNS)

    # 5. Check EMD involved
    emd_inv = any(p.search(text_clean) for p in _EMD_PATTERNS)

    # 6. Primary Reason & Summary
    if missing_docs:
        primary = missing_docs[0].name
    elif technical_dev:
        primary = "Technical Specification Deviation"
    elif emd_inv:
        primary = "EMD / Bid Security"
    else:
        primary = "Technical Disqualification"

    summary_parts = []
    if missing_docs:
        summary_parts.append(f"Missing documents: {', '.join(d.name for d in missing_docs)}")
    if technical_dev:
        summary_parts.append("Technical specification deviation noted")
    if emd_inv:
        summary_parts.append("EMD / Bid security issue")
    summary = "; ".join(summary_parts) or "Disqualified during technical evaluation."

    # 7. Formulate Rebuttal Points based on SellerProfile
    rebuttal_points: list[str] = []

    if emd_inv or any("MSE" in d.name for d in missing_docs):
        if profile and profile.is_mse:
            rebuttal_points.append(
                "The bidder is a registered Micro/Small Enterprise (MSE) under Udyam Registration. "
                "Under GeM GTC and Public Procurement Policy for MSEs Order, registered MSEs are exempt "
                "from payment of EMD / Bid Security and prior turnover/experience criteria for items produced by themselves."
            )

    if any("OEM Authorisation" in d.name for d in missing_docs):
        if profile and profile.is_oem:
            rebuttal_points.append(
                "The bidder is the Original Equipment Manufacturer (OEM) of the offered product category. "
                "Per GeM GTC guidelines, an OEM is not required to submit third-party authorization. "
                "OEM self-declaration certificate is enclosed."
            )

    if any("Turnover" in d.name for d in missing_docs):
        if profile and profile.annual_turnover_rupees:
            rebuttal_points.append(
                f"The bidder's average annual turnover is ₹{profile.annual_turnover_rupees:,}, duly certified by a Chartered Accountant. "
                "CA certified turnover certificates and audited balance sheets for the relevant financial years are attached."
            )

    if any("Experience" in d.name or "Past Performance" in d.name for d in missing_docs):
        if profile and profile.years_experience:
            rebuttal_points.append(
                f"The bidder possesses {profile.years_experience} years of commercial experience in executing government/commercial contracts. "
                "Copies of past supply orders and satisfactory completion certificates are attached."
            )

    if any("ITR" in d.name for d in missing_docs):
        if profile and profile.itr_filed_on_gem:
            rebuttal_points.append(
                "Income Tax Returns for the last 3 assessment years have already been filed and verified on GeM portal. "
                "Acknowledgement copies are attached."
            )

    # 8. Challenge Draft
    draft = draft_challenge(
        bid_number=bid_number,
        evaluation_date=eval_date,
        buyer_reason=text_clean,
        rebuttal_points=rebuttal_points,
        missing_docs=missing_docs,
    )

    return DisqualificationAnalysis(
        bid_number=bid_number,
        raw_text=text_clean,
        evaluation_date=eval_date,
        challenge_deadline_date=deadline_date,
        deadline_text=deadline_str,
        missing_docs=missing_docs,
        primary_reason=primary,
        summary=summary,
        emd_involved=emd_inv,
        technical_deviation=technical_dev,
        has_rebuttal=bool(rebuttal_points),
        rebuttal_points=rebuttal_points,
        challenge_draft=draft,
    )


def check_rejection_warnings(
    required_docs: Sequence[str],
    past_rejections: Sequence[dict],
) -> list[dict]:
    """Given a list of required documents for an upcoming bid or checklist, checks if the seller

    was previously disqualified for any of them. Emits actionable warnings.
    """
    warnings: list[dict] = []
    for doc in required_docs:
        doc_lower = doc.lower()
        for rej in past_rejections:
            rej_doc = rej.get("missing_doc", "")
            if rej_doc and (rej_doc.lower() in doc_lower or doc_lower in rej_doc.lower()):
                warnings.append({
                    "missing_doc": rej_doc,
                    "bid_number": rej.get("bid_number", ""),
                    "reason_text": rej.get("reason_text", ""),
                    "warning": f"Previous bid {rej.get('bid_number', '')} was rejected for '{rej_doc}'. Double-check this document before submitting!",
                })
    return warnings
