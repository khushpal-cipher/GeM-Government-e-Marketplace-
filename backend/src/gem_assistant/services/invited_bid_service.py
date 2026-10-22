"""Step 1.6: check the bids GeM invited him to. A bid already known is shown straight away; an
unknown number is looked up with one public listing search per batch, borrowing a discovery run's
guard rails (one run at a time, the 15-minute gap, contact email, breaker, daily budget), and only
the card with exactly that bid number is downloaded."""

from __future__ import annotations

from typing import Callable, Sequence

from ..domain.invited_bids import BID_NUMBER, parse_invited_bids
from ..domain.ports import ListingSource
from ..safety.errors import SafetyError
from .discovery_service import DiscoveryNotAllowed

MAX_PER_LOOKUP = 10


class InvitedBidService:
    def __init__(self, bids, listings, fetch_service, discovery, source_factory: Callable[[], ListingSource], clock):
        self._bids = bids
        self._listings = listings
        self._fetch = fetch_service
        self._discovery = discovery
        self._source_factory = source_factory
        self._clock = clock

    def _status(self, number: str) -> dict:
        bid_id = self._bids.find_id_by_bid_number(number)
        if bid_id is not None:
            return {"status": "ANALYSED", "bid_id": bid_id}
        entry = self._listings.find_by_bid_number(number)
        return {"status": "LISTED" if entry else "NEEDS_LOOKUP"}

    def parse(self, text: str) -> list[dict]:
        return [{"bid_number": b.bid_number, "raw_line": b.raw_line,
                 "extended_to": b.extended_to.isoformat() if b.extended_to else None, **self._status(b.bid_number)}
                for b in parse_invited_bids(text)]

    def import_bids(self, bid_numbers: Sequence[str]) -> list[dict]:
        numbers = list(dict.fromkeys(n.strip().upper() for n in bid_numbers if n.strip()))
        if len(numbers) > MAX_PER_LOOKUP:
            raise ValueError(f"At most {MAX_PER_LOOKUP} bids at a time (GeM request budget).")
        bad = [n for n in numbers if not BID_NUMBER.match(n)]
        if bad:
            raise ValueError(f"Not a GeM bid number: {', '.join(bad)} (like GEM/2026/B/1234567)")

        results = {n: self._status(n) for n in numbers}
        unknown = [n for n, r in results.items() if r["status"] == "NEEDS_LOOKUP"]
        if unknown:
            try:
                run = self._discovery.run(trigger="invited", keywords=unknown,
                                          execute=lambda r: self._search(r.keywords))
            except DiscoveryNotAllowed as error:
                for n in unknown:
                    results[n] = {"status": "NOT_STARTED", "message": str(error)}
                return [{"bid_number": n, **results[n]} for n in numbers]
            if run.outcome != "ok":
                for n in unknown:
                    results[n] = {"status": "FAILED", "message": run.message}
                return [{"bid_number": n, **results[n]} for n in numbers]

        for n in numbers:
            if results[n]["status"] == "ANALYSED":
                continue
            entry = self._listings.find_by_bid_number(n)  # exact number only, never a loose match
            if entry is None:
                results[n] = {"status": "NOT_FOUND", "message": "GeM's public bid list has no bid with this number."}
                continue
            try:
                fetched = self._fetch.fetch_listing_entry(entry)
            except SafetyError as error:
                results[n] = {"status": "NOT_STARTED", "message": str(error)}
                continue
            results[n] = ({"status": "ANALYSED", "bid_id": fetched.import_result.id} if fetched
                          else {"status": "FAILED", "message": "The bid document could not be read."})
        return [{"bid_number": n, **results[n]} for n in numbers]

    def _search(self, keywords: list[str]) -> None:
        now = self._clock.now()
        for result in self._source_factory().search(keywords, 1):
            self._listings.upsert(result.bids, result.keyword, now)
