"""Reads a GeM marketplace product page and its "Other Sellers" summary (step 6.3)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal
from html.parser import HTMLParser


class _Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        self._skip += tag in ("script", "style")

    def handle_endtag(self, tag):
        self._skip -= tag in ("script", "style")

    def handle_data(self, data):
        if not self._skip:
            self.parts.append(data)


def _text(html: str) -> str:
    reader = _Text()
    reader.feed(html)
    return " ".join(" ".join(reader.parts).split())


def _rupees(text: str) -> Decimal | None:
    found = re.search(r"₹\s*([\d,]+(?:\.\d+)?)", text)
    return Decimal(found.group(1).replace(",", "")) if found else None


@dataclass(frozen=True)
class ProductPage:
    mrp: Decimal | None
    offer_price: Decimal | None


@dataclass(frozen=True)
class SellersSummary:
    offerings: int | None
    price_low: Decimal | None
    price_high: Decimal | None


def parse_product(html: str) -> ProductPage:
    text = _text(html)
    mrp = re.search(r"MRP/Unit:\s*(₹\s*[\d,]+(?:\.\d+)?)", text)
    offer = re.search(r"Offer Price/Unit:\s*(₹\s*[\d,]+(?:\.\d+)?)", text)
    return ProductPage(_rupees(mrp.group(1)) if mrp else None, _rupees(offer.group(1)) if offer else None)


def parse_sellers_summary(html: str) -> SellersSummary:
    text = _text(html)
    count = re.search(r"Number of Seller Offerings:\s*([\d,]+)", text)
    prices = re.search(r"Price offered in the Range of:\s*(₹\s*[\d,]+(?:\.\d+)?)\s*-\s*(₹\s*[\d,]+(?:\.\d+)?)", text)
    return SellersSummary(int(count.group(1).replace(",", "")) if count else None,
                          _rupees(prices.group(1)) if prices else None, _rupees(prices.group(2)) if prices else None)
