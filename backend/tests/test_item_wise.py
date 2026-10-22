"""Step 3.6: an item-wise bid (real bid 9939006, "Item wise evaluation", 7 medicines) needs only some items."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from gem_assistant.api.app import create_app
from gem_assistant.domain.models import SellerProfile, matching_items
from gem_assistant.eligibility.rules import CategoryMatchRule

from .conftest import FIXTURES

PDF = FIXTURES / "GEM-bid-9939006_item-wise.pdf"


@pytest.fixture
def client(container):
    return TestClient(create_app(container, allowed_hosts=frozenset({"testserver"})))


def _bid(container):
    result = container.bid_import.import_pdf(PDF.read_bytes(), "item-wise.pdf")
    return container.bid_query.get(result.id).bid, result.id


def test_item_wise_bid_is_judged_item_by_item_so_one_matching_item_is_enough(container):
    bid, _ = _bid(container)
    assert bid.found_value("evaluation_method") == "Item wise evaluation"
    rule = CategoryMatchRule()
    # He sells one of the 7 medicines: no "you must quote all items" review (that is for total-value bids).
    assert rule.evaluate(bid, SellerProfile(categories=["Nitrofurantoin"]), None) == []
    (r,) = rule.evaluate(bid, SellerProfile(categories=["Laptop"]), None)
    assert "None of the items" in r.reason


def test_the_bid_page_lists_his_items(container, client):
    _, bid_id = _bid(container)
    container.profiles.save(SellerProfile(categories=["Nitrofurantoin", "Clonazepam"]))
    detail = client.get(f"/api/bids/{bid_id}").json()
    assert detail["your_items"] == ["Nitrofurantoin 100mg", "Clonazepam 0.5 mg Tab"]
    assert detail["item_count"] == 7


def test_matching_items_keeps_order_and_respects_ignore_words():
    text = "Office Chair, Chair Cover, Table"
    assert matching_items(text, ["chair"]) == ["Office Chair", "Chair Cover"]
    assert matching_items(text, ["chair"], ["cover"]) == ["Office Chair"]
