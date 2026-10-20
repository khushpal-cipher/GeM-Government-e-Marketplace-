"""Wording rules for everything the app drafts or reminds (docs/wording-rules.md).

Drafts go to government buyers under the seller's name, and he sends them himself: every draft says
so, never claims the app acted, never promises an outcome, and never carries PAN or bank details.
Deadlines always show the date (and time, if GeM gives one) in Indian time plus what is left.
"""

from __future__ import annotations

import re
from datetime import date, datetime, timedelta, timezone

IST = timezone(timedelta(hours=5, minutes=30))

DRAFT_NOTE = ("DRAFT - check every line before you send it yourself on GeM. "
              "The app has not sent, uploaded or submitted anything.")

# One alternation, longest first, so "you will definitely win" is one finding, not two.
_FORBIDDEN = re.compile(
    r"(?<!\w)(on your behalf|for you"
    r"|(?:the app|gem assistant) (?:has |have )?(?:sent|submitted|uploaded|accepted|paid|filed)"
    r"|(?:sent|submitted|uploaded|accepted|paid|filed) automatically"
    r"|you are eligible|you will (?:definitely |surely )?win|guaranteed?|100 ?%)(?!\w)",
    re.IGNORECASE)
_PAN = re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b")
_IFSC = re.compile(r"\b[A-Z]{4}0[A-Z0-9]{6}\b")


def check_draft(text: str) -> list[str]:
    """Problems with a draft; empty means it follows the rules."""
    problems = [] if text.lstrip().startswith(DRAFT_NOTE) else ["must start with the draft note"]
    problems += [f"says “{m.group(0)}”: the app never acts for him or promises an outcome"
                 for m in _FORBIDDEN.finditer(text)]
    if _PAN.search(text):
        problems.append("contains a PAN; leave it out, GeM already has it")
    if _IFSC.search(text):
        problems.append("contains an IFSC/bank detail; leave it out")
    return problems


def _day(d: date) -> str:
    return f"{d:%a} {d.day} {d:%b %Y}"


def _time(t: datetime) -> str:
    return f"{t.hour % 12 or 12}:{t.minute:02d} {'AM' if t.hour < 12 else 'PM'}"


def _n(count: int, unit: str) -> str:
    return f"{count} {unit}{'' if count == 1 else 's'}"


def deadline(due: date | datetime, now: datetime) -> str:
    """'by Fri 23 Oct 2026, 5:00 PM (3 days left)'. A date alone means the end of that day."""
    today = now.astimezone(IST).date()
    if not isinstance(due, datetime):
        days = (due - today).days
        if days < 0:
            return f"missed: was due {_day(due)} ({_n(-days, 'day')} ago)"
        if days <= 1:
            return f"by {'today' if days == 0 else 'tomorrow'}, {_day(due)}"
        return f"by {_day(due)} ({_n(days, 'day')} left)"

    if due.tzinfo is None:
        raise ValueError("a deadline time needs its time zone")
    local = due.astimezone(IST)
    days = (local.date() - today).days
    if due <= now:
        when = "today" if days == 0 else _day(local.date())
        ago = "" if days == 0 else f" ({_n(-days, 'day')} ago)"
        return f"missed: was due {when}, {_time(local)}{ago}"
    if days >= 2:
        return f"by {_day(local.date())}, {_time(local)} ({_n(days, 'day')} left)"
    hours = int((due - now).total_seconds() // 3600)
    left = "less than 1 hour left" if hours < 1 else f"{_n(hours, 'hour')} left"
    when = "today" if days == 0 else f"tomorrow, {_day(local.date())}"
    return f"by {when}, {_time(local)} ({left})"
