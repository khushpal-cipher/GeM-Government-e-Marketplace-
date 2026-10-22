"""Step 7.5: listing pre-check on values he types."""

from decimal import Decimal

from gem_assistant.domain.listing_check import check_listing

PROOF = "Price list 2026: JK Excel A4 copier paper, MRP Rs 1,200.00 per ream"


def _run(**over):
    args = dict(price=Decimal("1080"), mrp=Decimal("1200"), photos=3, brand="JK", model="Excel A4", mrp_proof_text=PROOF)
    return {r["check"]: r for r in check_listing(**{**args, **over})}


def test_good_listing_passes_everything():
    assert all(r["ok"] for r in _run().values())


def test_price_must_be_10_percent_below_mrp_and_not_above():
    assert _run(price=Decimal("1081"))["price"]["ok"] is False and "1080.00" in _run(price=Decimal("1100"))["price"]["message"]
    assert _run(price=Decimal("1300"))["price"]["ok"] is False


def test_fewer_than_three_photos_fails():
    assert _run(photos=2)["photos"]["ok"] is False


def test_model_that_repeats_brand_or_blank_fails():
    assert _run(brand="JK", model="jk")["brand_model"]["ok"] is False
    assert _run(model="")["brand_model"]["ok"] is False


def test_proof_must_name_brand_model_and_mrp():
    assert _run(mrp_proof_text="Invoice for stationery, total 99")["mrp_proof"]["ok"] is False
    assert _run(mrp_proof_text="")["mrp_proof"]["ok"] is None
    assert _run(brand="Camlin")["mrp_proof"]["ok"] is False
