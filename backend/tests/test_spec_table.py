"""Step 2.2: the specification table ("Specification / Bid Requirement (Allowed Values)") as rows."""

from __future__ import annotations

from gem_assistant.infrastructure.pypdf_extractor import PypdfTextExtractor
from gem_assistant.parsing.evidence import quote_is_on_page
from gem_assistant.parsing.spec_table import read_specifications

from .conftest import FIXTURES

OFFICE = FIXTURES / "GEM-2026-B-8054438_doc9913333.pdf"      # 4 items, one table each
CARTRIDGE = FIXTURES / "GEM-2026-B-8142835_doc10014519.pdf"  # the same table on 4 pages
LAPTOP = FIXTURES / "GEM-2026-B-8105558_doc9971825.pdf"


def _rows(path):
    data = path.read_bytes()
    pages = PypdfTextExtractor(max_pages=300).extract(data)
    return pages, read_specifications(data, pages)


def test_rows_have_group_name_and_value_across_wrapped_lines():
    _, rows = _rows(OFFICE)
    by_name = {(r.page, r.name): r for r in rows}
    row = by_name[(5, "Frame material for work station")]
    assert (row.group, row.value) == ("MATERIAL", "Aluminium")
    long = by_name[(8, "Backrest Height (Low-back range: 200 - 400 mm, Mid-back range: 401 - 700 mm, "
                       "High-back range: equal to or more than 701 mm)")]
    assert long.value == "Mid-back"


def test_group_carries_over_to_rows_without_a_label():
    _, rows = _rows(OFFICE)
    row = next(r for r in rows if r.page == 7 and r.name.startswith("Material of Table Understructure"))
    assert row.group == "Table Understructure"
    assert row.value == "Mild Steel, Aluminium Or higher"


def test_repeated_table_is_kept_per_page():
    _, rows = _rows(CARTRIDGE)
    colours = [(r.page, r.value) for r in rows if r.name == "Color of the Ink/Toner"]
    assert colours == [(3, "Black"), (4, "Magenta"), (5, "Cyan"), (6, "Yellow")]
    models = next(r for r in rows if r.name == "Model Number of OEM's Printer/OEM's Multi Function Machine")
    assert models.value.endswith("MFP Z36") and models.value.startswith("TX-5300")


def test_every_quote_is_on_its_page():
    for path in (OFFICE, CARTRIDGE, LAPTOP):
        pages, rows = _rows(path)
        assert all(quote_is_on_page(r.evidence, pages) for r in rows), path.name


def test_page_without_table_gives_no_rows():
    _, rows = _rows(LAPTOP)
    assert all(r.page != 1 for r in rows)
