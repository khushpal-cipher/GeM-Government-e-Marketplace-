"""Step 6.3: can he win a direct order at his price? Reads a product's public page and its "Other Sellers"
summary (2 GeM requests). GeM's public summary has only the offer count and the price range, not where each
seller delivers (looked at 23 Oct 2026), so it cannot say who undercuts him at the buyer's location. Advice only."""

from __future__ import annotations

import re
from decimal import ROUND_CEILING, Decimal
from urllib.parse import urlsplit

from ..parsing.product_parser import parse_product, parse_sellers_summary
from ..safety.response_classifier import Expect

_PATH = re.compile(r"^(/[\w\-]+){2}/p-\d+-\d+-cat(\.html|/all_sellers\.html)?$")


def _inr(value: Decimal) -> str:
    return f"₹{value:,.2f}"


class DirectOrderService:
    def __init__(self, fetcher):
        self._fetcher = fetcher

    def check(self, link: str, target_price: Decimal) -> dict:
        parts = urlsplit(link.strip())
        if parts.scheme != "https" or parts.hostname != "mkp.gem.gov.in" or not _PATH.match(parts.path):
            raise ValueError("Paste a product link from mkp.gem.gov.in (it ends in -cat.html).")
        if target_price <= 0:
            raise ValueError("The price must be more than zero.")
        base = "https://mkp.gem.gov.in" + re.sub(r"(\.html|/all_sellers\.html)$", "", parts.path)
        product = parse_product(self._get(base + ".html"))
        sellers = parse_sellers_summary(self._get(base + "/all_sellers.html"))
        floor = (product.mrp * Decimal("0.9")).quantize(Decimal("0.01"), ROUND_CEILING) if product.mrp else None

        if floor is not None and target_price < floor:
            verdict = (f"{_inr(target_price)} is more than 10% below the MRP ({_inr(product.mrp)}). "
                       f"The lowest you can list is {_inr(floor)}.")
        elif sellers.price_low is None:
            verdict = "GeM's page did not show the price range, so there is nothing to compare with."
        elif target_price < sellers.price_low:
            verdict = f"{_inr(target_price)} is lower than every listing ({_inr(sellers.price_low)} is the lowest)."
        else:
            verdict = (f"Someone lists as low as {_inr(sellers.price_low)}. GeM's public page does not show "
                       "where each seller delivers, so check the buyer's location on GeM yourself.")
        return {"mrp": str(product.mrp) if product.mrp else None, "lowest_he_can_list": str(floor) if floor else None,
                "offerings": sellers.offerings,
                "price_low": str(sellers.price_low) if sellers.price_low else None,
                "price_high": str(sellers.price_high) if sellers.price_high else None,
                "verdict": verdict,
                "warning": "Once you list for a place you must deliver any order that comes from it."}

    def _get(self, url: str) -> str:
        return self._fetcher.get(url, expect=Expect.PRODUCT_PAGE).body.decode("utf-8", errors="replace")
