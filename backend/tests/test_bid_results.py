"""Step 6.1: the public result page of a finished bid (fixture shaped like the real page seen 22-23 Oct 2026)."""

from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import pytest

from gem_assistant.domain.ports import HttpResponse
from gem_assistant.infrastructure.database import Database
from gem_assistant.infrastructure.sqlite_repositories import SqliteBidResultRepository
from gem_assistant.parsing.result_parser import parse_result
from gem_assistant.safety.response_classifier import Expect, ResponseClassifier, ResponseKind
from gem_assistant.services.result_service import MAX_PER_DAY, ResultLimitReached, ResultService

FIX = Path(__file__).parent / "fixtures"
HTML = (FIX / "bid-result-8506455_2026-10-23.html").read_text()
EMPTY = (FIX / "bid-result-not-evaluated_2026-10-23.html").read_text()


def test_reads_bidders_prices_and_l1():
    r = parse_result(HTML)
    assert (r.bid_number, r.status, r.quantity) == ("GEM/2025/B/6819518", "Cancelled", 6383)
    assert [(b.seller, b.qualified) for b in r.bidders] == [
        ("SELLER ONE", False), ("SELLER TWO", True), ("SELLER THREE", True), ("SELLER FOUR", False)]
    assert [(p.seller, p.total_price, p.rank) for p in r.prices] == [
        ("SELLER THREE", Decimal("817024.00"), "L1"), ("SELLER TWO", Decimal("865491.53"), "L2")]
    assert r.l1.seller == "SELLER THREE"


def test_bid_not_evaluated_yet_has_no_rows():
    r = parse_result(EMPTY)
    assert (r.status, r.bidders, r.prices, r.l1) == ("Active", [], [], None)


def _kind(body: str) -> ResponseKind:
    return ResponseClassifier().classify(HttpResponse("https://bidplus.gem.gov.in/x", 200, {}, body.encode()),
                                         Expect.RESULT_PAGE).kind


def test_page_with_captcha_in_scripts_is_not_a_block():
    assert "captcha" in HTML.lower()
    assert _kind(HTML) is ResponseKind.OK


def test_challenge_page_is_a_block():
    assert _kind("<html><body>Please solve the captcha</body></html>") is ResponseKind.BLOCK


class _Fetcher:
    def __init__(self):
        self.urls = []

    def get(self, url, expect):
        self.urls.append((url, expect))
        return HttpResponse(url, 200, {}, HTML.encode())


class _Clock:
    def now(self):
        return datetime(2026, 10, 23, 12, 0, tzinfo=timezone.utc)


@pytest.fixture
def service(tmp_path):
    db = Database(tmp_path / "t.db")
    db.migrate()
    fetcher = _Fetcher()
    return ResultService(fetcher, SqliteBidResultRepository(db), _Clock()), fetcher


def test_read_fetches_once_then_serves_from_storage(service):
    svc, fetcher = service
    first = svc.read("8506455")
    assert svc.read("8506455") == first
    assert fetcher.urls == [("https://bidplus.gem.gov.in/bidding/bid/getBidResultView/8506455", Expect.RESULT_PAGE)]
    assert first["l1_seller"] == "SELLER THREE" and first["l1_price"] == "817024.00"
    assert first["prices"][1]["rank"] == "L2"


def test_packet_kinds_pick_the_right_path(service):
    svc, fetcher = service
    svc.read("1", "single")
    svc.read("2", "multi")
    assert [u.rsplit("/", 2)[1] for u, _ in fetcher.urls] == ["getSinglePacketResultView", "getBidResultViewSchedule"]


@pytest.mark.parametrize("doc_id,packets", [("12a", ""), ("", ""), ("1", "other")])
def test_refuses_bad_input(service, doc_id, packets):
    with pytest.raises(ValueError):
        service[0].read(doc_id, packets)


def test_daily_limit(service):
    svc, fetcher = service
    for n in range(MAX_PER_DAY):
        svc.read(str(n + 1))
    with pytest.raises(ResultLimitReached):
        svc.read("999")
    assert len(fetcher.urls) == MAX_PER_DAY
