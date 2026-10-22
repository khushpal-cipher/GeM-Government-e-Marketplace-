"""Delivery state from a PIN's first two digits (India Post zones), and his state names matched to them."""

from __future__ import annotations

import re

_DD = "Dadra and Nagar Haveli and Daman and Diu"
_NE = ("Arunachal Pradesh", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Tripura")
_BY_PREFIX: dict[int, tuple[str, ...]] = {
    11: ("Delhi",), 12: ("Haryana",), 13: ("Haryana",), 14: ("Punjab",), 15: ("Punjab",),
    16: ("Punjab", "Chandigarh"), 17: ("Himachal Pradesh",), 18: ("Jammu and Kashmir",),
    19: ("Jammu and Kashmir", "Ladakh"), 24: ("Uttar Pradesh", "Uttarakhand"),
    26: ("Uttar Pradesh", "Uttarakhand"), 36: ("Gujarat", _DD), 37: ("Gujarat",), 38: ("Gujarat",),
    39: ("Gujarat", _DD), 40: ("Maharashtra", "Goa"), 49: ("Chhattisgarh",), 50: ("Telangana",),
    53: ("Andhra Pradesh", "Puducherry"), 60: ("Tamil Nadu", "Puducherry"), 67: ("Kerala", "Puducherry"),
    68: ("Kerala", "Lakshadweep"), 69: ("Kerala",), 73: ("West Bengal", "Sikkim"),
    74: ("West Bengal", "Andaman and Nicobar"), 78: ("Assam",), 79: _NE,
    80: ("Bihar",), 84: ("Bihar",), 85: ("Bihar",),
}
for _prefixes, _states in (((20, 21, 22, 23, 25, 27, 28), ("Uttar Pradesh",)), ((30, 31, 32, 33, 34), ("Rajasthan",)),
                           ((41, 42, 43, 44), ("Maharashtra",)), ((45, 46, 47, 48), ("Madhya Pradesh",)),
                           ((51, 52), ("Andhra Pradesh",)), ((56, 57, 58, 59), ("Karnataka",)),
                           ((61, 62, 63, 64), ("Tamil Nadu",)), ((70, 71, 72), ("West Bengal",)),
                           ((75, 76, 77), ("Odisha",)), ((81, 82, 83), ("Bihar", "Jharkhand"))):
    _BY_PREFIX.update({p: _states for p in _prefixes})

_ALIASES = {
    "up": "Uttar Pradesh", "mp": "Madhya Pradesh", "ap": "Andhra Pradesh", "hp": "Himachal Pradesh",
    "uk": "Uttarakhand", "uttaranchal": "Uttarakhand", "tn": "Tamil Nadu", "wb": "West Bengal",
    "jk": "Jammu and Kashmir", "jandk": "Jammu and Kashmir", "jammu kashmir": "Jammu and Kashmir", "delhi": "Delhi", "nct of delhi": "Delhi",
    "new delhi": "Delhi", "orissa": "Odisha", "pondicherry": "Puducherry", "cg": "Chhattisgarh",
    "chattisgarh": "Chhattisgarh", "dnhdd": _DD, "daman and diu": _DD, "dadra and nagar haveli": _DD,
    "andaman": "Andaman and Nicobar", "andaman and nicobar islands": "Andaman and Nicobar",
}
KNOWN_STATES = {s for states in _BY_PREFIX.values() for s in states} | {"Kerala"}


def states_for_pin(pin: str | None) -> set[str]:
    """Empty when the PIN is masked, malformed, or in a zone this table doesn't cover (Army Post Office...)."""
    if not pin or not re.fullmatch(r"\d{6}", pin):
        return set()
    return set(_BY_PREFIX.get(int(pin[:2]), ()))


def normalise_states(names: list[str]) -> tuple[set[str], list[str]]:
    """(known states, names no alias knows)."""
    known: set[str] = set()
    unknown: list[str] = []
    by_lower = {s.lower(): s for s in KNOWN_STATES}
    for name in names:
        k = re.sub(r"\s+", " ", re.sub(r"[^a-z& ]", "", name.lower().replace(".", ""))).strip().replace("&", "and")
        k = re.sub(r"\s+", " ", k)
        state = by_lower.get(k) or _ALIASES.get(k)
        (known.add(state) if state else unknown.append(name))
    return known, unknown
