"""Step 6.1: reads the public result page of a finished bid (who qualified, prices, L1) and keeps it.
One public GET per bid, at most MAX_PER_DAY new pages a day; a bid already read is served from storage."""

from __future__ import annotations

from ..parsing.result_parser import parse_result
from ..safety.response_classifier import Expect

MAX_PER_DAY = 10
_PATHS = {"single": "getSinglePacketResultView", "multi": "getBidResultViewSchedule", "": "getBidResultView"}


class ResultLimitReached(Exception):
    pass


class ResultService:
    def __init__(self, fetcher, repo, clock):
        self._fetcher = fetcher
        self._repo = repo
        self._clock = clock

    def read(self, doc_id: str, packets: str = "") -> dict:
        """packets: "" (GeM's default page), "single" or "multi" (when the listing says b_eval_type > 0)."""
        if not doc_id.isdigit() or packets not in _PATHS:
            raise ValueError("A GeM bid document number (digits only) is needed.")
        stored = self._repo.get(doc_id)
        if stored:
            return stored
        now = self._clock.now()
        if self._repo.count_since(now.replace(hour=0, minute=0, second=0, microsecond=0)) >= MAX_PER_DAY:
            raise ResultLimitReached(f"At most {MAX_PER_DAY} result pages a day (GeM request budget).")
        response = self._fetcher.get(f"https://bidplus.gem.gov.in/bidding/bid/{_PATHS[packets]}/{doc_id}",
                                     expect=Expect.RESULT_PAGE)
        self._repo.save(doc_id, parse_result(response.body.decode("utf-8", errors="replace")), now)
        return self._repo.get(doc_id)
