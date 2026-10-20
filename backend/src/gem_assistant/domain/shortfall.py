"""Step 1.3: shortfall-reply helper (docs/wording-rules.md, progress.md step 1.3).

From a pasted clarification from GeM (e.g. from Bids -> List of Bids -> Already participated ->
Clarification History), this helper:
1. Extracts the bid number, due date, and buyer's query.
2. Identifies each requested document using deterministic patterns.
3. Checks against the seller's profile (1.1) to see which documents he has or needs to obtain.
4. Drafts a formal covering note following 1.0 wording rules (starts with DRAFT_NOTE, quotes
   the buyer, uses bracketed placeholders like [attach: OEM authorisation], and never claims the app acted).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime
from typing import Sequence

from .gem_alerts import _DATE, _REF, MONTHS
from .models import SellerProfile
from .wording import DRAFT_NOTE, deadline


@dataclass(frozen=True)
class RequestedDocument:
    name: str
    quote: str
    in_profile: bool | None
    profile_note: str
    placeholder: str


@dataclass(frozen=True)
class ShortfallReply:
    bid_number: str | None
    due: date | None
    due_text: str | None
    documents: list[RequestedDocument]
    draft: str
    clarification_text: str


# Deterministic patterns for documents asked in GeM clarifications.
# (pattern, name, placeholder)
_DOC_PATTERNS: list[tuple[re.Pattern, str, str]] = [
    # OEM specific
    (re.compile(r"(?:OEM|Original Equipment Manufacturer)\s+(?:annual\s+)?turnover(?:\s+for\s+(?:last\s+)?(?:\d+\s+)?years?)?", re.IGNORECASE),
     "OEM Turnover", "[attach: OEM turnover for last 3 years]"),
    (re.compile(r"(?:OEM|Original Equipment Manufacturer|Manufacturer(?:'s)?)\s+(?:authorisation|authorization|maf|auth\b)", re.IGNORECASE),
     "OEM Authorisation", "[attach: OEM authorisation]"),

    # Tax & Registration
    (re.compile(r"\bGST\s*(?:certificate|registration|return)?\b", re.IGNORECASE),
     "GST Certificate", "[attach: GST registration certificate]"),
    (re.compile(r"\b(?:ITR|income\s+tax\s+returns?)\b(?:\s+(?:acknowledgements?|copies|returns?))?(?:\s+for\s+(?:last\s+)?(?:\d+\s+)?years?)?", re.IGNORECASE),
     "Income Tax Returns (ITR)", "[attach: ITR acknowledgement copies for last 3 years]"),
    (re.compile(r"\b(?:MSME|MSE|Udyam|Udyog\s+Aadhaar)\s*(?:certificate|registration)?\b", re.IGNORECASE),
     "MSE / Udyam Certificate", "[attach: Udyam registration certificate]"),
    (re.compile(r"\b(?:Startup|DPIIT|DIPP)\s*(?:certificate|recognition)?\b", re.IGNORECASE),
     "Startup / DPIIT Certificate", "[attach: DPIIT startup recognition certificate]"),

    # Experience & Turnover
    (re.compile(r"\b(?:past\s+performance|experience\s+criteria|experience\s+certificate|completion\s+certificate|past\s+experience|supply\s+orders?|work\s+orders?)\b", re.IGNORECASE),
     "Past Performance / Experience", "[attach: past performance / experience certificates]"),
    (re.compile(r"\b(?:bidder|seller|firm|company|annual|ca)\s+turnover\b|\bturnover\s+certificate\b|\baverage\s+annual\s+turnover\b|\bturnover\s+for\s+(?:last\s+)?(?:\d+\s+)?years?\b", re.IGNORECASE),
     "Bidder Annual Turnover", "[attach: CA certified annual turnover certificate]"),

    # Certifications
    (re.compile(r"\bISO\s*\d+(?::\d+)?(?:\s+certificate|\s+certification)?\b", re.IGNORECASE),
     "ISO Certificate", "[attach: ISO certificate]"),
    (re.compile(r"\bBIS\s*(?:certificate|certification)?\b", re.IGNORECASE),
     "BIS Certificate", "[attach: BIS certificate]"),
    (re.compile(r"\b(?:CE|RoHS)\s*(?:certificate|certification)?\b", re.IGNORECASE),
     "Standards Certificate", "[attach: Standards compliance certificate]"),

    # Technical Compliance
    (re.compile(r"\b(?:technical\s+compliance|compliance\s+sheet|compliance\s+statement|clause[- ]by[- ]clause)\b", re.IGNORECASE),
     "Technical Compliance Sheet", "[attach: signed technical compliance sheet]"),

    # Declarations / Undertakings
    (re.compile(r"\b(?:make\s+in\s+india|mii|land\s+border|non[- ]blacklisting|no[- ]debarment|integrity\s+pact|undertaking|declaration)\b", re.IGNORECASE),
     "Declaration / Undertaking", "[attach: signed declaration / undertaking]"),

    # Bank / Cheque
    (re.compile(r"\b(?:cancelled\s+cheque|bank\s+mandate|pfms\s+mandate|bank\s+details)\b", re.IGNORECASE),
     "Bank Details / Cancelled Cheque", "[attach: cancelled cheque / bank mandate]"),
]

# Fallback pattern for any "submit / upload / provide / furnish <something>"
_GENERIC_DOC = re.compile(
    r"\b(?:submit|upload|furnish|provide|attach|submit\s+copy\s+of|provide\s+copy\s+of)\s+([a-zA-Z0-9\s,-]+?)(?:\.|\band\b|$)",
    re.IGNORECASE)


def _check_profile_for_doc(name: str, quote: str, profile: SellerProfile) -> tuple[bool | None, str]:
    """Matches a requested document against what is recorded in SellerProfile."""
    if name == "OEM Authorisation":
        if profile.is_oem or profile.oem_products:
            return True, "You are registered as OEM; attach self-authorisation or OEM declaration."
        return False, "Reseller profile: obtain authorization from the OEM."

    if name == "OEM Turnover":
        if profile.is_oem:
            if profile.annual_turnover_rupees:
                return True, f"OEM profile: recorded turnover is ₹{profile.annual_turnover_rupees:,}."
            return False, "OEM profile, but no annual turnover recorded."
        return False, "Reseller profile: obtain CA turnover certificate from the OEM."

    if name == "Bidder Annual Turnover":
        if profile.annual_turnover_rupees is not None:
            return True, f"Profile shows annual turnover ₹{profile.annual_turnover_rupees:,}; attach CA certificate."
        return False, "No annual turnover recorded in profile; attach CA certificate."

    if name == "Past Performance / Experience":
        if profile.years_experience is not None:
            return True, f"Profile shows {profile.years_experience} years experience; attach past performance copies."
        return False, "No experience years recorded in profile; attach past performance contracts."

    if name == "MSE / Udyam Certificate":
        if profile.is_mse:
            return True, "Profile says MSE is Yes; attach Udyam registration certificate."
        return False, "Profile says not MSE; Udyam certificate missing."

    if name == "Startup / DPIIT Certificate":
        if profile.is_startup:
            return True, "Profile says Startup is Yes; attach DPIIT certificate."
        return False, "Profile says not Startup; DPIIT certificate missing."

    if name == "GST Certificate":
        if any("gst" in c.lower() for c in profile.certifications):
            return True, "Profile lists GST in certifications."
        return False, "Not listed in profile certifications; attach GST certificate."

    if name == "Income Tax Returns (ITR)":
        if profile.itr_filed_on_gem is True:
            return True, "ITR is recorded as filed on GeM; attach acknowledgement copies."
        return False, "ITR status on GeM is unconfirmed; attach ITR acknowledgements."

    if name == "Bank Details / Cancelled Cheque":
        if profile.pfms_bank_verified is True:
            return True, "Bank account is PFMS-verified on GeM; attach cancelled cheque."
        return False, "Bank account PFMS verification unconfirmed; attach cancelled cheque."

    if "ISO" in name or name == "BIS Certificate" or name == "Standards Certificate":
        # Check against profile.certifications
        norm_cert = "iso" if "ISO" in name else ("bis" if "BIS" in name else name.lower())
        matched = next((c for c in profile.certifications if norm_cert in c.lower()), None)
        if matched:
            return True, f"Profile lists '{matched}' in certifications."
        return False, f"Missing from profile certifications: attach {name}."

    if name == "Technical Compliance Sheet":
        return None, "Bid-specific document: fill, sign and attach."

    if name == "Declaration / Undertaking":
        return None, "Standard declaration on firm letterhead: sign and attach."

    return False, "Not matched to a standard profile detail: check and attach manually."


def detect_documents(text: str, profile: SellerProfile | None = None) -> list[RequestedDocument]:
    """Finds documents asked in clarification text using deterministic patterns."""
    profile = profile or SellerProfile()
    found: list[RequestedDocument] = []
    seen_names: set[str] = set()
    matched_spans: list[tuple[int, int]] = []

    # 1. Match known patterns
    for pattern, name, placeholder in _DOC_PATTERNS:
        for match in pattern.finditer(text):
            span = match.span()
            if any(max(span[0], s[0]) < min(span[1], s[1]) for s in matched_spans):
                continue
            # Special case: don't match Bidder Turnover if it's actually OEM Turnover
            preceding = text[:span[0]].rstrip()
            if name == "Bidder Annual Turnover" and (preceding.lower().endswith("oem") or "OEM Turnover" in seen_names):
                continue
            actual_name = name
            if "ISO" in name:
                actual_name = f"{match.group(0).strip().upper()} Certificate"
                placeholder = f"[attach: {match.group(0).strip().upper()} certificate]"
            quote = match.group(0).strip()
            in_profile, note = _check_profile_for_doc(name, quote, profile)
            found.append(RequestedDocument(
                name=actual_name,
                quote=quote,
                in_profile=in_profile,
                profile_note=note,
                placeholder=placeholder,
            ))
            seen_names.add(name)
            matched_spans.append(span)
            break

    # 2. Fallback: if nothing matched or additional generic requests
    if not found:
        for match in _GENERIC_DOC.finditer(text):
            candidate = match.group(1).strip()
            # Clean up trailing punctuation
            candidate = candidate.strip(",. ")
            if len(candidate) > 3 and candidate.lower() not in {"the following", "documents", "clarification"}:
                in_profile, note = _check_profile_for_doc("Generic", candidate, profile)
                found.append(RequestedDocument(
                    name=candidate.title(),
                    quote=candidate,
                    in_profile=in_profile,
                    profile_note=note,
                    placeholder=f"[attach: {candidate}]",
                ))

    return found


def _clean_query_text(text: str) -> str:
    """Strips metadata header lines to extract the actual buyer query."""
    lines = []
    for line in text.splitlines():
        line_str = line.strip()
        if not line_str:
            continue
        lower = line_str.lower()
        if (lower.startswith("clarification history")
                or lower.startswith("bid no:")
                or lower.startswith("request no")
                or lower.startswith("status:")):
            continue
        lines.append(line_str)
    return " ".join(lines) if lines else text.strip()


def draft_covering_note(clarification_text: str,
                        documents: Sequence[RequestedDocument],
                        profile: SellerProfile | None = None,
                        bid_number: str | None = None) -> str:
    """Drafts the formal covering note to the buyer following 1.0 wording rules."""
    profile = profile or SellerProfile()
    firm_name = profile.business_name.strip() if profile.business_name else "[your firm name]"
    bid_display = bid_number.strip() if bid_number else "[bid number]"
    quoted_query = _clean_query_text(clarification_text)

    attachment_lines = []
    if documents:
        for i, d in enumerate(documents, start=1):
            attachment_lines.append(f"{i}. {d.placeholder}")
    else:
        attachment_lines.append("1. [attach: requested documents]")

    attachments_block = "\n".join(attachment_lines)

    draft = (
        f"{DRAFT_NOTE}\n\n"
        f"To: Buyer / Bid Committee, Bid {bid_display}\n"
        f"Subject: Submission of documents against clarification request\n\n"
        f"Dear Sir/Madam,\n\n"
        f"With reference to your clarification request:\n"
        f'"{quoted_query}"\n\n'
        f"We submit herewith the following requested documents:\n"
        f"{attachments_block}\n\n"
        f"Kindly accept these documents for technical evaluation.\n\n"
        f"Yours faithfully,\n"
        f"{firm_name}"
    )
    return draft


def _find_date(text: str) -> date | None:
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


def shortfall_reply(text: str,
                    profile: SellerProfile | None = None,
                    bid_number: str | None = None,
                    due: date | None = None,
                    now: datetime | None = None) -> ShortfallReply:
    """Full shortfall helper: extracts metadata, detects documents, and drafts covering note."""
    profile = profile or SellerProfile()
    now = now or datetime.now()

    # Extract bid number if not given
    if not bid_number:
        ref_match = _REF.search(text)
        if ref_match:
            bid_number = ref_match.group(0).upper()

    # Extract due date if not given
    if not due:
        due = _find_date(text)

    due_text = deadline(due, now) if due else None
    documents = detect_documents(text, profile)
    draft = draft_covering_note(text, documents, profile, bid_number)

    return ShortfallReply(
        bid_number=bid_number,
        due=due,
        due_text=due_text,
        documents=documents,
        draft=draft,
        clarification_text=text.strip(),
    )
