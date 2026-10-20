"""The daily GeM check: text he pastes from his own GeM account (the app never logs in) becomes
alerts with a due date. Dates come from GeM's own rules (HANDOFF §4a); a date the text doesn't
give is never guessed, it is left empty and shown back to him to fill in."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, timedelta

MONTHS = {m: i for i, m in enumerate(
    ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"), start=1)}


@dataclass(frozen=True)
class Kind:
    label: str
    ask: str          # what he opens on GeM and pastes
    where: str        # where he acts on GeM
    if_missed: str
    days_after: int   # due = the date pasted + this many days


KINDS = {
    "clarification": Kind(
        "Buyer asks for documents", "Bids → List of Bids → Already participated → Clarification History: paste the request",
        "Bids → List of Bids → Already participated → Pending Clarifications",
        "the buyer can reject your bid on technical grounds", 0),
    "acceptance": Kind(
        "Order waiting for acceptance", "Orders: paste the order line (contract number and date)",
        "Orders → the order → accept or decline",
        "it is accepted automatically after 120 hours (declining or missing some orders freezes that product's stock for 15 days)", 5),
    "delivery": Kind(
        "Order near its delivery date", "Orders → the order → Consignee/Shipment tab: paste the expected delivery date",
        "Orders → the order → create the invoice",
        "the order expires and invoicing is disabled; late delivery costs 0.5% of the late value per week", 0),
    "payment": Kind(
        "Goods received, payment not made", "Orders → shipment Details: paste the line with the CRAC date",
        "Incidents → New → delay in payment (GeM's last step is a letter to the buyer's senior officers)",
        "late payment goes unchallenged; the buyer owes 1% interest per month", 10),
    "scn": Kind(
        "Show-cause notice", "Incidents: paste the notice line with its date",
        "Incidents → the notice → reply",
        "no reply means automatic action by severity (up to suspension)", 10),
}

_REF = re.compile(r"GEM/\d{4}/[A-Z]/\d+|GEMC-\d+", re.IGNORECASE)
_DATE = re.compile(
    r"\b(?P<d>\d{1,2})(?:st|nd|rd|th)?[-/ ](?:(?P<m>\d{1,2})|(?P<mon>[A-Za-z]{3})[a-z]*)[-/ ,]*(?P<y>\d{4})\b"
    r"|\b(?P<y2>\d{4})-(?P<m2>\d{2})-(?P<d2>\d{2})\b")


@dataclass(frozen=True)
class AlertDraft:
    kind: str
    ref: str
    text: str
    due: date | None
    unclear: str | None


def _first_date(text: str) -> date | None:
    for m in _DATE.finditer(text):
        try:
            if m.group("y2"):
                return date(int(m.group("y2")), int(m.group("m2")), int(m.group("d2")))
            month = int(m.group("m")) if m.group("m") else MONTHS.get(m.group("mon").lower())
            if month:
                return date(int(m.group("y")), month, int(m.group("d")))
        except ValueError:
            continue  # 31-02-2026 and the like: look at the next date
    return None


def parse_paste(kind: str, text: str) -> list[AlertDraft]:
    """One draft per bid or contract number, each with the text up to the next number."""
    rule = KINDS[kind]
    text = text.strip()
    if not text:
        return []
    found = list(_REF.finditer(text))
    if not found:
        segments = [("", text)]
    else:
        # Text before the first number belongs to the first item (e.g. a heading line).
        starts = [0] + [m.start() for m in found[1:]]
        ends = starts[1:] + [len(text)]
        segments = [(m.group(0).upper(), text[s:e].strip()) for m, s, e in zip(found, starts, ends)]
    drafts = []
    for ref, segment in segments:
        base = _first_date(segment)
        due = base + timedelta(days=rule.days_after) if base else None
        problems = ([] if ref else ["no bid or contract number found"]) + ([] if due else ["no date found"])
        drafts.append(AlertDraft(kind, ref, segment, due, "; ".join(problems) or None))
    return drafts
