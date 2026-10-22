"""Reads the "Technical Specifications" table of a bid PDF: group, specification name, allowed value.

Plain text loses which wrapped line belongs to which column, so this reads the position of each
text piece: group at the left (x < 100), name in the middle, value at the right (x >= 300).
Lines closer than 20 units belong to one row. A row is kept only if its quote is on the page.
"""

from __future__ import annotations

import io
import re
from typing import Sequence

from pypdf import PdfReader

from ..domain.models import Evidence, ExtractionMethod, PageText, SpecRow
from .evidence import quote_is_on_page

_UNREADABLE = re.compile(r"[ऀ-ॿ\x00-\x08\x0b-\x1f]")
_FOOTER = re.compile(r"\d+ / \d+")
_NAME_X, _VALUE_X, _ROW_GAP, _LINE_GAP = 100, 300, 20, 16


def read_specifications(pdf_bytes: bytes, pages: Sequence[PageText]) -> list[SpecRow]:
    wanted = {p.number for p in pages if "Allowed Values" in p.text}
    if not wanted:
        return []
    reader = PdfReader(io.BytesIO(pdf_bytes))
    rows: list[SpecRow] = []
    group = ""
    for number in sorted(wanted):
        for body, closed in _tables(reader.pages[number - 1]):
            table_rows, group = _page_rows(number, body, group)
            rows.extend(r for r in table_rows if quote_is_on_page(r.evidence, pages))
            if closed:  # the item's consignee table follows: the next table is another item
                group = ""
    return rows


def _tables(page) -> list[tuple[list[tuple[float, float, str]], bool]]:
    """The spec tables on a page: (pieces below the "(Allowed Values)" header, ended by the consignee table)."""
    found: list[tuple[float, float, str]] = []

    def visit(text, cm, tm, font_dict, font_size):
        piece = text.strip()
        if piece and "\n" not in text and not _UNREADABLE.search(piece):
            found.append((tm[4], tm[5], piece))

    page.extract_text(visitor_text=visit)
    tables: list[tuple[list[tuple[float, float, str]], bool]] = []
    body: list[tuple[float, float, str]] | None = None
    for piece in found:
        if piece[2] == "(Allowed Values)":
            if body is not None:
                tables.append((body, False))
            body = []
        elif body is not None and piece[2].startswith("/Consignees"):
            tables.append((body, True))
            body = None
        elif body is not None and not _FOOTER.fullmatch(piece[2]):
            body.append(piece)
    if body is not None:
        tables.append((body, False))
    return tables


def _join(parts) -> str:
    # A line that ends in a hyphen was wrapped inside a word ("Mid-" / "back"): no space.
    out = ""
    for _, _, text in parts:
        wrapped = out.endswith("-") and not out.endswith(" -")
        out += text if not out or wrapped else " " + text
    return out


def _page_rows(number: int, pieces, group: str) -> tuple[list[SpecRow], str]:
    cells = sorted((p for p in pieces if p[0] >= _NAME_X), key=lambda p: p[1])
    labels = sorted((p for p in pieces if p[0] < _NAME_X), key=lambda p: p[1])
    blocks: list[list[tuple[float, float, str]]] = []
    for cell in cells:
        if blocks and cell[1] - blocks[-1][-1][1] < _ROW_GAP:
            blocks[-1].append(cell)
        else:
            blocks.append([cell])
    rows: list[SpecRow] = []
    for i, block in enumerate(blocks):
        top = block[0][1]
        limit = blocks[i + 1][0][1] if i + 1 < len(blocks) else float("inf")
        own = [p for p in labels if top - 3 <= p[1] < limit]
        if own:  # a group label starts here (it may wrap onto the next lines)
            group = " ".join(p[2] for p in own)
        name_parts = [p for p in block if p[0] < _VALUE_X]
        value_parts = [p for p in block if p[0] >= _VALUE_X]
        name = _join(name_parts)
        value = _join(value_parts)
        if name and value:
            quote = "\n".join([*(p[2] for p in name_parts), *(p[2] for p in value_parts)])
            rows.append(SpecRow(group=group, name=name, value=value, evidence=Evidence(
                page=number, quote=quote, method=ExtractionMethod.LABEL_PARSE)))
    return rows, group
