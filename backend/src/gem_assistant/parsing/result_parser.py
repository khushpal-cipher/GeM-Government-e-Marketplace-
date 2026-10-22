"""Reads GeM's public bid result page (getBidResultView and friends): who qualified, prices, L1 (step 6.1)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from decimal import Decimal
from html.parser import HTMLParser


@dataclass(frozen=True)
class Bidder:
    seller: str          # the firm name as GeM shows it
    offered: str
    qualified: bool | None  # None when GeM shows neither word


@dataclass(frozen=True)
class RankedPrice:
    seller: str
    total_price: Decimal  # rupees
    rank: str             # "L1", "L2", ...
    item: str = ""        # what the price is for, as GeM shows it


@dataclass(frozen=True)
class BidResult:
    bid_number: str | None
    status: str | None
    quantity: int | None
    bidders: list[Bidder] = field(default_factory=list)
    prices: list[RankedPrice] = field(default_factory=list)

    @property
    def l1(self) -> RankedPrice | None:
        return next((p for p in self.prices if p.rank == "L1"), None)


class _Tables(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tables: list[list[list[str]]] = []
        self.text: list[str] = []
        self._cell: list[str] | None = None
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1
        elif tag == "table":
            self.tables.append([])
        elif tag == "tr" and self.tables:
            self.tables[-1].append([])
        elif tag in ("td", "th") and self.tables and self.tables[-1]:
            self._cell = []

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip -= 1
        elif tag in ("td", "th") and self._cell is not None:
            self.tables[-1][-1].append(" ".join("".join(self._cell).split()))
            self._cell = None

    def handle_data(self, data):
        if self._skip:
            return
        if self._cell is not None:
            self._cell.append(data)
        self.text.append(data)


def _firm(name: str) -> str:
    return re.sub(r"\s*\(MSE.*$|\s+Under PMA$", "", name).strip()


def parse_result(html: str) -> BidResult:
    reader = _Tables()
    reader.feed(html)
    text = " ".join(" ".join(reader.text).split())

    def grab(pattern: str) -> str | None:
        found = re.search(pattern, text)
        return found.group(1) if found else None

    quantity = grab(r"Quantity:\s*([\d,]+)")
    bidders: list[Bidder] = []
    prices: list[RankedPrice] = []
    for table in reader.tables:
        header = [c.lower() for c in table[0]] if table else []
        for row in table[1:]:
            if len(row) != len(header):
                continue  # the empty closing row
            cells = dict(zip(header, row))
            if "status" in cells and "participated on" in cells:
                word = cells["status"].lower()
                bidders.append(Bidder(_firm(cells["seller name"]), cells["offered item"],
                                      {"qualified": True, "disqualified": False}.get(word)))
            elif "total price" in cells and "rank" in cells:
                amount = re.search(r"[\d,]+(?:\.\d+)?", cells["total price"])
                if amount:
                    prices.append(RankedPrice(_firm(cells["seller name"]),
                                              Decimal(amount.group().replace(",", "")), cells["rank"],
                                              re.sub(r"^Item Categories\s*:\s*", "", cells["offered item"])))
    return BidResult(grab(r"Bid Number:\s*(GEM/\d{4}/\w/\d+)"), grab(r"Bid Status:\s*(\w[\w ]*?)\s+Quantity"),
                     int(quantity.replace(",", "")) if quantity else None, bidders, prices)
