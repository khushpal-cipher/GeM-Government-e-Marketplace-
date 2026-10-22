"""Step 2.5b: asks Groq to read a bid's buyer terms, at most once per text and 15 times a day.

Only on request. The reply is stored as Groq sent it and checked again on every use, so a
stricter check later applies to old replies too. Any failure reads as "not read, check yourself".
"""

from __future__ import annotations

import hashlib
from typing import Protocol, Sequence

from ..domain import atc_reading
from ..domain.atc_reading import AtcReading
from ..domain.models import PageText
from ..domain.ports import Clock
from ..infrastructure.groq_chat import ChatModelError
from ..infrastructure.sqlite_repositories import SqliteAtcReadingRepository
from ..safety.daily_budget import IST

DAILY_AI_READS = 15  # ~7,400 tokens each: ~110K of Groq's 200K a day, the rest is left for the chat


class JsonModel(Protocol):
    model: str

    def read_json(self, body: dict) -> str: ...


class AtcReadingService:
    def __init__(self, model: JsonModel, replies: SqliteAtcReadingRepository, clock: Clock,
                 daily_limit: int = DAILY_AI_READS):
        self._model = model
        self._replies = replies
        self._clock = clock
        self._daily_limit = daily_limit

    def read(self, bid_pages: Sequence[PageText], atc_file_pages: Sequence[PageText] = ()) -> AtcReading:
        prepared = atc_reading.prepare(bid_pages, atc_file_pages)
        if not prepared.pages:
            return AtcReading("read", notes=["This bid has no buyer-added terms for the AI to read."])
        key = hashlib.sha256(f"{atc_reading.PROMPT_VERSION}|{self._model.model}|{prepared.text}".encode()).hexdigest()
        for raw in self._replies.replies(key):
            reading = atc_reading.check_reply(raw, prepared)
            if reading.status == "read":
                return reading
        now = self._clock.now()
        start_of_day = now.astimezone(IST).replace(hour=0, minute=0, second=0, microsecond=0)
        if self._replies.count_since(start_of_day) >= self._daily_limit:
            return atc_reading.not_read(prepared, f"The AI has read {self._daily_limit} bids' terms today, the daily "
                                                  "limit; read them yourself or ask again tomorrow.")
        body = atc_reading.build_request(prepared, self._model.model, atc_reading.new_boundary())
        try:
            raw = self._model.read_json(body)
        except ChatModelError as error:
            return atc_reading.not_read(prepared, f"{atc_reading.NOT_READ} ({error})")
        self._replies.add(key, raw, now)
        return atc_reading.check_reply(raw, prepared)
