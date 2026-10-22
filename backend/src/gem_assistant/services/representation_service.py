"""Step 7.1: a draft question to the buyer (GeM "Representation") about terms GeM's list says a bid may not carry.
He reads it and sends it himself on GeM; the app sends nothing. Wording follows docs/wording-rules.md."""

from __future__ import annotations

from datetime import date

from ..domain.wording import DRAFT_NOTE, check_draft, deadline
from ..eligibility.rules import _FORBIDDEN, representation_deadline


class RepresentationService:
    def __init__(self, bid_query, profiles, clock):
        self._bids, self._profiles, self._clock = bid_query, profiles, clock

    def draft(self, bid_id: int) -> dict | None:
        item = self._bids.get(bid_id)
        if item is None:
            return None
        bid, now = item.bid, self._clock.now()
        flags = [f for f in bid.flags if f.category in _FORBIDDEN]
        if not flags:
            return {"draft": None, "message": "No term from GeM's list of forbidden terms was flagged in this bid."}

        number = bid.bid_number or "[bid number]"
        profile = self._profiles.get()
        firm = (profile.business_name if profile and profile.business_name else "[your firm name]")
        lines = [DRAFT_NOTE, "", "To,", "The Buyer / Competent Authority,", "",
                 f"Subject: Request to review term(s) in Bid No. {number}", "", "Respected Sir/Madam,", "",
                 f"With reference to Bid No. {number}, we request you to review the following term(s). They appear to "
                 "fall in GeM's list of terms that should not be included in a bid:", ""]
        for n, flag in enumerate(flags, start=1):
            list_no, list_text = _FORBIDDEN[flag.category]
            lines += [f"{n}. Bid document, page {flag.evidence.page}: “{flag.evidence.quote}”",
                      f"   GeM's list, item {list_no}: {list_text}.", ""]
        lines += ["We request that the term(s) be removed or modified so that all eligible sellers can take part on "
                  "equal terms. Kindly answer through GeM before the bid closes.", "",
                  "Thanking you,", "Yours faithfully,", firm]
        draft = "\n".join(lines)

        dated, end = bid.found_value("bid_dated"), bid.deadline()
        last = representation_deadline(date.fromisoformat(dated), end) if dated and end else None
        return {"draft": draft, "problems": check_draft(draft),
                "last_date": deadline(last, now) if last else "date unknown; check on GeM",
                "where": "Bids → open the bid → Representation",
                "if_missed": "you bid on the term as written, or skip the bid",
                "note": "GeM allows one representation per bid."}
