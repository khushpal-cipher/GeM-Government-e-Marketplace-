"""Step 7.2: a compliance sheet for a bid: each line of the buyer's specification table, what his product offers
(from the key specs he typed in, step 3.9) and yes / no / fill in. He checks it and uploads it himself on GeM."""

from __future__ import annotations

from ..domain.models import item_match
from ..domain.wording import DRAFT_NOTE, check_draft
from ..eligibility.rules import _norm, spec_allows


class ComplianceService:
    def __init__(self, bid_query, profiles):
        self._bids, self._profiles = bid_query, profiles

    def sheet(self, bid_id: int) -> dict | None:
        item = self._bids.get(bid_id)
        if item is None:
            return None
        bid, profile = item.bid, self._profiles.get()
        if not bid.specifications:
            return {"sheet": None, "message": "No specification table was read from this bid."}
        products = profile.products if profile else []
        product = next((p for p in products
                        if item_match(bid.found_value("item_category"), [p.name], profile.ignore_words)[0]), None)
        mine = {_norm(k): (k, v) for k, v in (product.specs if product else {}).items()}
        rows = []
        for spec in bid.specifications:
            offer = mine.get(_norm(spec.name), (None, None))[1]
            fits = spec_allows(spec.value, offer) if offer is not None else None
            rows.append({"spec": spec.name, "buyer_wants": spec.value, "page": spec.page, "offer": offer,
                         "answer": "yes" if fits else "no" if fits is False else "fill in"})
        lines = [DRAFT_NOTE, "", f"Compliance sheet, Bid No. {bid.bid_number or '[bid number]'}"
                 + (f", product: {product.name}" if product else ""), "",
                 "Specification | Buyer asks | Our offer | Complies"]
        lines += [f"{r['spec']} | {r['buyer_wants']} | {r['offer'] or '[fill in]'} | {r['answer']}" for r in rows]
        sheet = "\n".join(lines)
        return {"product": product.name if product else None, "rows": rows, "sheet": sheet,
                "problems": check_draft(sheet),
                "note": "Only specs you typed for the product are filled; check every line against the bid."}
