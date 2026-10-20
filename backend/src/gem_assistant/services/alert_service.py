"""Alerts from the daily GeM check: parse what he pasted, keep what he confirms, list what is open."""

from __future__ import annotations

from datetime import date

from ..domain.gem_alerts import KINDS, AlertDraft, parse_paste
from ..domain.ports import Clock
from ..domain.wording import IST, deadline


class AlertService:
    def __init__(self, repo, clock: Clock):
        self._repo = repo
        self._clock = clock

    def preview(self, kind: str, text: str) -> list[AlertDraft]:
        return parse_paste(kind, text)

    def add(self, kind: str, items: list[dict]) -> int:
        now = self._clock.now()
        return sum(self._repo.add(kind, i["ref"].strip().upper(), i["text"].strip(), i["due"], now) for i in items)

    def open(self) -> list[dict]:
        now = self._clock.now()
        out = []
        for row in self._repo.open():
            kind = KINDS[row["kind"]]
            due = date.fromisoformat(row["due"]) if row["due"] else None
            out.append({**row, "label": kind.label, "where": kind.where, "if_missed": kind.if_missed,
                        "due_text": deadline(due, now) if due else "date unknown",
                        "overdue": bool(due and due < now.astimezone(IST).date())})
        return out

    def done(self, alert_id: int) -> bool:
        return self._repo.done(alert_id, self._clock.now())
