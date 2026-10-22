"""Does a bid deliver to a city he works in? Judged from the consignee addresses in the bid."""

from __future__ import annotations

import re
from typing import Sequence

from .models import Consignee


def delivers_to_cities(consignees: Sequence[Consignee], cities: Sequence[str]) -> bool | None:
    """True / False, or None when it cannot be judged: no cities set, no table, or every address masked.
    shortcut: matches the city name as a whole word in the address text, so a spelling GeM writes
    differently (Gurugram / Gurgaon) is missed; he can list both."""
    if not cities:
        return None
    readable = [c.address for c in consignees if c.pin is not None]  # no PIN = the buyer masked the place
    if not readable:
        return None
    wanted = [re.compile(rf"(?<!\w){re.escape(city.strip())}(?!\w)", re.IGNORECASE) for city in cities if city.strip()]
    return any(w.search(a) for w in wanted for a in readable)
