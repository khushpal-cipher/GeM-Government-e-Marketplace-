"""Step 1.3: Service for shortfall-reply helper."""

from __future__ import annotations

from datetime import date

from ..domain.models import SellerProfile
from ..domain.ports import Clock
from ..domain.shortfall import ShortfallReply, shortfall_reply


class ShortfallService:
    def __init__(self, profiles, clock: Clock):
        self._profiles = profiles
        self._clock = clock

    def reply(self, text: str, bid_number: str | None = None, due: date | None = None) -> ShortfallReply:
        profile = self._profiles.get() or SellerProfile()
        return shortfall_reply(text, profile, bid_number, due, now=self._clock.now())
