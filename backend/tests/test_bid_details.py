"""Step 2.1: consignees and the other bid-form facts, on real bid documents."""

from __future__ import annotations

import pytest

from gem_assistant.domain.models import FieldStatus
from gem_assistant.infrastructure.pypdf_extractor import PypdfTextExtractor
from gem_assistant.parsing.consignee_table import check_quantity, read_consignees
from gem_assistant.parsing.evidence import quote_is_on_page
from gem_assistant.parsing.label_extractor import LabelFieldExtractor

from .conftest import FIXTURES

LAPTOP = FIXTURES / "GEM-2026-B-8105558_doc9971825.pdf"      # 1 consignee, 15 days
TWO_PACKET = FIXTURES / "GEM-2026-B-8054438_doc9913333.pdf"  # 4 tables, one per item
MASKED = FIXTURES / "GEM-2025-B-6819518_doc8506455.pdf"      # defence bid: officer and PIN masked
ITEM_WISE = FIXTURES / "GEM-2026-B-7922876_doc9762022.pdf"


def _pages(path):
    return PypdfTextExtractor(max_pages=300).extract(path.read_bytes())


def _fields(path):
    return {f.name: f for f in LabelFieldExtractor().extract(_pages(path))}


def test_single_consignee_row():
    (row,) = read_consignees(_pages(LAPTOP))
    assert (row.pin, row.quantity, row.delivery_days) == ("313001", 1, 15)
    assert "UDAIPUR" in row.address
    assert quote_is_on_page(row.evidence, _pages(LAPTOP))


def test_consignee_rows_of_every_item_table():
    rows = read_consignees(_pages(TWO_PACKET))
    assert [(r.quantity, r.delivery_days) for r in rows] == [(10, 15), (13, 15), (7, 15), (50, 15)]


def test_masked_rows_keep_the_place_name_and_no_pin():
    (row,) = read_consignees(_pages(MASKED))
    assert row.pin is None and "THIRUVALLUR" in row.address
    assert (row.quantity, row.delivery_days) == (6383, 180)


def test_item_wise_bid_has_one_row_per_schedule_item():
    rows = read_consignees(_pages(ITEM_WISE))
    assert [(r.quantity, r.delivery_days) for r in rows] == [(1, 180), (1, 180)]


@pytest.mark.parametrize("path,expected", [
    (LAPTOP, {"estimated_bid_value": "477900", "inspection_required": "No",
              "technical_clarification_days": "2",
              "documents_required": "Certificate (Requested in ATC),Compliance of BoQ specification "
                                    "and supporting document"}),
    (TWO_PACKET, {"past_performance_percent": "50", "inspection_required": "No"}),
])
def test_bid_form_facts(path, expected):
    fields = _fields(path)
    for name, value in expected.items():
        assert fields[name].status is FieldStatus.FOUND, name
        assert fields[name].value == value, name


def test_epbg_months_and_value_with_inr_label():
    fields = _fields(FIXTURES / "GEM-2026-B-8061591_doc9921669.pdf")
    assert fields["epbg_months"].value == "14"
    assert fields["estimated_bid_value"].value == "8500000"


def test_quantities_that_add_up_leave_the_total_alone():
    fields = list(_fields(LAPTOP).values())
    out = check_quantity(fields, read_consignees(_pages(LAPTOP)))
    assert next(f for f in out if f.name == "total_quantity").status is FieldStatus.FOUND


def test_quantities_that_do_not_add_up_become_conflicting():
    fields = list(_fields(TWO_PACKET).values())
    rows = read_consignees(_pages(TWO_PACKET))[:-1]  # one row lost
    total = next(f for f in check_quantity(fields, rows) if f.name == "total_quantity")
    assert total.status is FieldStatus.CONFLICTING
    assert "80" in total.note


def test_no_table_means_no_check():
    fields = list(_fields(LAPTOP).values())
    out = check_quantity(fields, [])
    assert next(f for f in out if f.name == "total_quantity").status is FieldStatus.FOUND


def test_consignees_are_saved_and_read_back(container):
    result = container.bid_import.import_pdf(TWO_PACKET.read_bytes(), source_name="bid.pdf")
    bid = container.bid_query.get(result.id).bid
    assert [(c.quantity, c.delivery_days) for c in bid.consignees] == [(10, 15), (13, 15), (7, 15), (50, 15)]
    assert bid.consignees[0].evidence.page >= 1
    assert next(f for f in bid.fields if f.name == "total_quantity").status is FieldStatus.FOUND
