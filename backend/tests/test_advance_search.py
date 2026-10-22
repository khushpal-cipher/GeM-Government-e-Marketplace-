"""Step 4.2 rest: Advance Search through the page's own searchBid(), behind the same guards."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from urllib.parse import parse_qs

from gem_assistant.domain.ports import HttpResponse
from gem_assistant.infrastructure.browser_listing import PlaywrightListingSource
from gem_assistant.safety.url_policy import UrlPolicy
from tests.listing_fixtures import make_doc, make_response
from tests.test_listing import _chromium, browser_test

SHELL = (Path(__file__).parent / "fixtures" / "advance-search-shell_2026-10-23.html").read_bytes()


class FakeAdvanceGeM:
    def __init__(self, docs):
        self.docs = docs
        self.requests = []  # (method, path, payload)

    def fetch(self, route):
        request = route.request
        path = "/" + request.url.split("gem.gov.in/", 1)[1]
        form = parse_qs(request.post_data or "")
        payload = json.loads(form["payload"][0]) if "payload" in form else None
        self.requests.append((request.method, path, payload))

        def reply(body, ctype):
            return HttpResponse(url=request.url, status=200, headers={"content-type": ctype}, body=body)

        if request.method == "GET":
            return reply(SHELL, "text/html")
        if path == "/state-list-adv":
            return reply(b'{"status":200,"data":[{"state_name":"RAJASTHAN"},{"state_name":"BIHAR"}]}', "application/json")
        if path == "/boq-title-adv":
            return reply(b'{"status":200,"data":[{"bbt_title":"Laptop"},{"bbt_title":""}]}', "application/json")
        start = (payload["page"] - 1) * 10
        body = make_response(self.docs[start:start + 10], total=len(self.docs), start=start)
        return reply(json.dumps(body).encode(), "application/json")


def _source(container, gem):
    return PlaywrightListingSource(fetcher=container.fetcher, network=gem, executable_path=_chromium(),
                                   timeout_seconds=20)


def test_the_three_advance_paths_are_post_only_and_nothing_else_is(settings):
    safety = settings.safety
    policy = UrlPolicy(safety.allowed_host_suffix, safety.blocked_path_prefixes,
                       safety.post_allowed_paths, safety.post_allowed_prefixes)
    for path in ("/search-bids", "/state-list-adv", "/boq-title-adv"):
        policy.check(f"https://bidplus.gem.gov.in{path}", "POST")


@browser_test
def test_state_search_sends_the_pages_own_payload_and_pages_through(container):
    gem = FakeAdvanceGeM([make_doc(i) for i in range(1, 15)])
    result = _source(container, gem).advance_search(
        "con", date(2026, 10, 23), date(2026, 10, 31), max_pages=2, state="RAJASTHAN")
    assert (result.total_found, len(result.bids)) == (14, 14)
    assert [(m, p) for m, p, _ in gem.requests] == [
        ("GET", "/advance-search"), ("POST", "/search-bids"), ("POST", "/search-bids")]
    first, second = (r[2] for r in gem.requests[1:])
    assert first["searchType"] == "con" and first["state_name_con"] == "RAJASTHAN"
    assert (first["bidEndFromCon"], first["bidEndToCon"], first["page"]) == ("2026-10-23", "2026-10-31", 1)
    assert second["page"] == 2 and second["state_name_con"] == "RAJASTHAN"


@browser_test
def test_boq_title_search(container):
    gem = FakeAdvanceGeM([make_doc(1)])
    result = _source(container, gem).advance_search(
        "boq", date(2026, 10, 23), date(2026, 10, 31), max_pages=1, boq_title="Laptop")
    assert len(result.bids) == 1
    assert gem.requests[1][2]["boqtitle_con"] == "Laptop"


@browser_test
def test_dropdown_lists_cost_two_requests(container):
    gem = FakeAdvanceGeM([])
    lists = _source(container, gem).advance_lists()
    assert lists == {"states": ["BIHAR", "RAJASTHAN"], "boq_titles": ["Laptop"]}
    assert [(m, p) for m, p, _ in gem.requests] == [
        ("GET", "/advance-search"), ("POST", "/state-list-adv"), ("POST", "/boq-title-adv")]


def test_a_search_without_its_main_box_is_refused_before_any_request(container):
    import pytest
    gem = FakeAdvanceGeM([])
    with pytest.raises(ValueError):
        _source(container, gem).advance_search("con", date(2026, 10, 23), date(2026, 10, 31), 1)
    assert gem.requests == []
