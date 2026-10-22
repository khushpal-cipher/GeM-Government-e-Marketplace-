"""Reads the "Consignees/Reporting Officer and Quantity" table of a bid PDF (recon §2).

pypdf gives one cell per line: serial number, officer name (1-2 lines), "<PIN>,<address>"
(several lines, a line may be only digits when the PIN wraps), quantity, delivery days.
Defence bids mask officer and PIN with asterisks. Rows are read per page; a row that
can't be read is left out, and the quantity check against "Total Quantity" then fails
loudly instead of guessing.
"""

from __future__ import annotations

import re
from typing import Sequence

from ..domain.models import Consignee, Evidence, ExtractedField, ExtractionMethod, FieldStatus, PageText

_HEADER = re.compile(r"^/Delivery\nDays$", re.MULTILINE)
_NUMBER = re.compile(r"\d+")
_FOOTER = re.compile(r"\d+ / \d+")  # "4 / 11": page number
_ADDRESS_START = re.compile(r"^(?:(?P<pin>\d{6}),|\*{3,})")


def read_consignees(pages: Sequence[PageText]) -> list[Consignee]:
    rows: list[Consignee] = []
    carry = False  # the previous page ended with a table header: its rows start this page
    for page in pages:
        lines = page.text.split("\n")
        starts = [page.text[:m.end()].count("\n") + 1 for m in _HEADER.finditer(page.text)]
        for start in [0, *starts] if carry else starts:
            rows.extend(_table(page.number, lines, start))
        carry = bool(starts) and all(_FOOTER.fullmatch(line) for line in lines[starts[-1]:])
    return rows


def _table(page: int, lines: list[str], i: int) -> list[Consignee]:
    rows: list[Consignee] = []
    serial = 1
    while i < len(lines) and lines[i] == str(serial):
        end = _row_end(lines, i + 1, serial)
        if end is None:
            break
        rows.append(_row(page, lines[i + 1:end]))
        i, serial = end, serial + 1
    return rows


def _row_end(lines: list[str], i: int, serial: int) -> int | None:
    """Index just past the delivery-days line: the first two number lines followed by
    the next serial + a name, a non-number line, or the end of the page."""
    for j in range(i + 2, len(lines) - 1):
        if not (_NUMBER.fullmatch(lines[j]) and _NUMBER.fullmatch(lines[j + 1])):
            continue
        after = lines[j + 2:j + 4]
        if (not after or not _NUMBER.fullmatch(after[0])
                or (after[0] == str(serial + 1) and len(after) > 1 and not _NUMBER.fullmatch(after[1]))):
            return j + 2
    return None


def _row(page: int, cells: list[str]) -> Consignee:
    *text, quantity, days = cells
    first = next((k for k in range(1, len(text)) if _ADDRESS_START.match(text[k])), 1)
    address = text[first:] or text
    pin = _ADDRESS_START.match(address[0])
    # The quote starts at the address: the officer's name is not repeated in our data.
    return Consignee(
        pin=pin.group("pin") if pin else None,
        address=" ".join(address),
        quantity=int(quantity),
        delivery_days=int(days),
        evidence=Evidence(page=page, quote="\n".join([*address, quantity, days]),
                          method=ExtractionMethod.LABEL_PARSE),
    )


def check_quantity(fields: list[ExtractedField], consignees: Sequence[Consignee]) -> list[ExtractedField]:
    """The consignee quantities must add up to "Total Quantity". If they don't, a row was lost
    or misread, so the total is marked CONFLICTING rather than trusted."""
    total = next((f for f in fields if f.name == "total_quantity"), None)
    if total is None or total.status is not FieldStatus.FOUND or not consignees:
        return fields
    added = sum(c.quantity for c in consignees)
    if added == int(total.value):
        return fields
    note = f"The consignee table adds up to {added}, the bid says {total.value}. A row may be unread."
    return [f.model_copy(update={"status": FieldStatus.CONFLICTING, "note": note}) if f is total else f
            for f in fields]
