"""Step 1.6: bid numbers from the invitations GeM shows on his dashboard (Notifications →
"You are invited to participate in bid (GEM/…)"), which he pastes; the app never logs in."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date

from .gem_alerts import _REF, _first_date

BID_NUMBER = re.compile(r"^GEM/\d{4}/[A-Z]/\d+$")
_EXTENDED = re.compile(r"extended\s+to|extension\s+date|valid\s+till|last\s+date", re.IGNORECASE)


@dataclass(frozen=True)
class InvitedBid:
    bid_number: str
    raw_line: str
    extended_to: date | None = None


def parse_invited_bids(text: str) -> list[InvitedBid]:
    """Each bid number once, in paste order, with the date it was extended to if a line says so."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    found: dict[str, InvitedBid] = {}
    for line in lines:
        for m in _REF.finditer(line):
            ref = m.group(0).upper()
            if not ref.startswith("GEM/"):
                continue  # contract numbers (GEMC-…) are orders, not invitations
            extended = _first_date(line[_EXTENDED.search(line).end():]) if _EXTENDED.search(line) else None
            first = found.get(ref)
            if first is None:
                found[ref] = InvitedBid(ref, line, extended)
            elif extended and not first.extended_to:  # "bid … extended to …" on a later line
                found[ref] = InvitedBid(ref, first.raw_line, extended)
    return list(found.values())
