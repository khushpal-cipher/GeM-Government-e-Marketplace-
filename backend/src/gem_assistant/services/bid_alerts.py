"""Alerts worked out from bids the app already holds (step 5.1). Nothing is stored: they are
recomputed from the stored bids and listings each time, so they cannot go stale or need a "done"."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from ..domain.models import Verdict
from ..domain.wording import deadline
from ..eligibility.rules import representation_deadline

SOON = timedelta(days=3)
LIST_EARLY = timedelta(days=2)  # GeM can take 48 h to approve a product listing


class BidAlerts:
    def __init__(self, bid_query, discovery, clock):
        self._bids, self._discovery, self._clock = bid_query, discovery, clock

    def list(self) -> list[dict]:
        now = self._clock.now()
        rows: list[tuple[datetime, dict]] = []

        def add(kind, label, ref, due, where, if_missed, text=""):
            rows.append((due, {"kind": kind, "id": None, "ref": ref, "text": text, "due": due.isoformat(),
                               "label": label, "where": where, "if_missed": if_missed,
                               "due_text": deadline(due, now), "overdue": False}))

        for item in self._bids.list():
            bid, end = item.bid, item.bid.deadline()
            if item.assessment.verdict is Verdict.BLOCKED or not end:
                continue
            if now < end <= now + SOON:
                add("bid_closing", "Bid closing soon", bid.bid_number, end, "Bids → open the bid",
                    "you cannot bid after it closes")
            dated = bid.found_value("bid_dated")
            last = representation_deadline(date.fromisoformat(dated), end) if dated else None
            if last and now < last <= now + SOON and any(f.category.startswith("forbidden_") for f in bid.flags):
                add("bid_representation", "Last day to ask the buyer to change a term", bid.bid_number, last,
                    "Bids → the bid → Representation", "you bid on the term as written, or skip the bid")

        for entry in self._discovery.status().listings:
            if not entry.matched_items or not entry.ends_at or entry.ends_at <= now:
                continue
            if entry.is_new:
                add("bid_new", "New bid for your products", entry.bid_number, entry.ends_at,
                    "Discover page", "the bid closes without you seeing it", entry.category or "")
            last_to_list = entry.ends_at - LIST_EARLY
            if now < last_to_list <= now + SOON:
                add("bid_list_product", "List your matching product (if not listed yet)", entry.bid_number,
                    last_to_list, "Catalogue → add your product", "GeM approval can take 48 hours, "
                    "so a product listed later may not count for this bid")
        return [row for _, row in sorted(rows, key=lambda r: r[0])]
