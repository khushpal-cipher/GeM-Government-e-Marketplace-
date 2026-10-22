"""Step 6.2: what similar items sold for before. Advice only: it reads the result pages already kept (6.1)
and never contacts GeM."""

from __future__ import annotations

from decimal import Decimal

from ..domain.models import matching_items

NOTE = ("Winning (L1) prices of finished bids whose item names all your words. 'Per piece' is the total divided by "
        "the bid's quantity, right only when the bid had one item. GeM says offered prices are not approved prices.")


class PastPriceService:
    def __init__(self, results):
        self._results = results

    def similar(self, item: str, limit: int = 10) -> dict:
        found = []
        for result in self._results.all():
            for price in result["prices"]:
                if price["rank"] != "L1" or not matching_items(price.get("item"), [item]):
                    continue
                total, quantity = Decimal(price["total_price"]), result["quantity"]
                found.append({"bid_number": result["bid_number"], "status": result["status"], "item": price["item"],
                              "quantity": quantity, "l1_total": str(total),
                              "per_piece": str((total / quantity).quantize(Decimal("0.01"))) if quantity else None})
        return {"item": item, "matches": found[:limit], "note": NOTE}
