"""Step 7.5: checks on a new product listing he is about to make on GeM, before he starts. Everything is typed
by him; nothing is fetched. GeM rules (docs/HANDOFF.md): offer at least 10% below MRP, 3 photos that match the
product, a document proving the MRP that names this product (SFAQ)."""

from __future__ import annotations

import re
from decimal import ROUND_CEILING, Decimal


def _words(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def check_listing(*, price: Decimal, mrp: Decimal, photos: int, brand: str, model: str, mrp_proof_text: str) -> list[dict]:
    """One result per check: {"check", "ok" (True / False / None = could not tell), "message"}."""
    floor = (mrp * Decimal("0.9")).quantize(Decimal("0.01"), ROUND_CEILING)
    results = []

    def add(check: str, ok: bool | None, message: str) -> None:
        results.append({"check": check, "ok": ok, "message": message})

    if price > mrp:
        add("price", False, f"Your price {price} is above the MRP {mrp}.")
    elif price <= mrp * Decimal("0.9"):
        add("price", True, f"{price} is at least 10% below the MRP {mrp}.")
    else:
        add("price", False, f"GeM wants an offer at least 10% below the MRP: {floor} or less for MRP {mrp}.")
    add("photos", photos >= 3, f"{photos} photo(s); GeM wants 3 that match the product." if photos < 3
        else f"{photos} photos; check each one shows this exact product.")
    if not brand.strip() or not model.strip():
        add("brand_model", False, "Brand and model must both be filled.")
    elif _words(model) <= _words(brand):
        add("brand_model", False, "The model repeats the brand; the model is the product's own name or number.")
    else:
        add("brand_model", True, "Brand and model are both given.")
    if not mrp_proof_text.strip():
        add("mrp_proof", None, "No MRP proof text given; open the proof and check it names this product and MRP.")
    else:
        proof = _words(mrp_proof_text)
        missing = [w for w in (brand, model) if w.strip() and not _words(w) <= proof]
        mrp_seen = re.sub(r"\.0+$", "", str(mrp)) in mrp_proof_text.replace(",", "")
        problems = ([f"“{w}” is not in the proof" for w in missing]
                    + ([] if mrp_seen else [f"the MRP {mrp} is not in the proof"]))
        add("mrp_proof", not problems, "The proof names the brand, model and MRP." if not problems
            else "Proof does not match: " + "; ".join(problems) + ".")
    return results
