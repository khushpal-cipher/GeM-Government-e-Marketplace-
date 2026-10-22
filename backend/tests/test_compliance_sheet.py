"""Step 7.2: compliance sheet for a bid: buyer's spec line -> his offer -> yes / no / fill in."""

from types import SimpleNamespace

from gem_assistant.domain.models import Evidence, ExtractionMethod, ProductSpec, SpecRow
from gem_assistant.domain.wording import DRAFT_NOTE, check_draft
from gem_assistant.services.compliance_service import ComplianceService


def _row(name, value, page=3):
    return SpecRow(group="", name=name, value=value,
                   evidence=Evidence(page=page, quote=f"{name} {value}", method=ExtractionMethod.PATTERN_SCAN))


def _service(rows, products):
    bid = SimpleNamespace(bid_number="GEM/2026/B/1234567", specifications=rows,
                          found_value=lambda name: "A4 Copier Paper" if name == "item_category" else None)
    bids = SimpleNamespace(get=lambda i: SimpleNamespace(bid=bid) if i == 1 else None)
    profiles = SimpleNamespace(get=lambda: SimpleNamespace(products=products, ignore_words=[]))
    return ComplianceService(bids, profiles)


PAPER = ProductSpec(name="A4 Copier Paper", specs={"GSM": "80", "Size": "A4", "Colour": "Blue"})


def test_each_buyer_line_gets_yes_no_or_fill_in():
    result = _service([_row("GSM", "70, 75, 80"), _row("Colour", "White"), _row("Brightness", "92 Or higher")],
                      [PAPER]).sheet(1)
    answers = {r["spec"]: (r["offer"], r["answer"]) for r in result["rows"]}
    assert answers == {"GSM": ("80", "yes"), "Colour": ("Blue", "no"), "Brightness": (None, "fill in")}
    assert result["rows"][0]["buyer_wants"] == "70, 75, 80" and result["rows"][0]["page"] == 3


def test_sheet_text_is_a_draft_and_passes_wording_check():
    result = _service([_row("GSM", "80")], [PAPER]).sheet(1)
    assert result["sheet"].startswith(DRAFT_NOTE) and result["problems"] == [] and check_draft(result["sheet"]) == []
    assert "GSM" in result["sheet"] and "yes" in result["sheet"]


def test_no_matching_product_means_all_fill_in_and_unknown_bid_is_none():
    svc = _service([_row("GSM", "80")], [ProductSpec(name="Pen", specs={"GSM": "1"})])
    assert [r["answer"] for r in svc.sheet(1)["rows"]] == ["fill in"] and svc.sheet(2) is None


def test_bid_without_spec_table_says_so():
    assert _service([], [PAPER]).sheet(1)["sheet"] is None


def test_make_model_hsn_list_one_row_per_boq_item_filled_from_his_product():
    bid = SimpleNamespace(bid_number="GEM/2026/B/9781965", specifications=[],
                          found_value=lambda n: "LOUNGE , OFFICE , A4 Copier Paper" if n == "item_category" else None)
    paper = ProductSpec(name="A4 Copier Paper", specs={"Make": "JK", "model": "Excel", "HSN": "4802"})
    svc = ComplianceService(SimpleNamespace(get=lambda i: SimpleNamespace(bid=bid)),
                            SimpleNamespace(get=lambda: SimpleNamespace(products=[paper], ignore_words=[])))
    result = svc.make_model_hsn(1)
    assert [r["item"] for r in result["rows"]] == ["LOUNGE", "OFFICE", "A4 Copier Paper"]
    assert result["rows"][2] == {"item": "A4 Copier Paper", "make": "JK", "model": "Excel", "hsn": "4802"}
    assert result["rows"][0]["make"] is None and result["problems"] == []
    assert result["sheet"].startswith(DRAFT_NOTE) and "[fill in]" in result["sheet"]
