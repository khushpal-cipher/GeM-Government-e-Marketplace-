"""Step 2.4: the documents one bid asks the seller to upload, each with page + quote.

Sources: the bid form's "Document required from seller" list, and the text of the files
the bid PDF links to (buyer ATC file, specification PDF) when they were read as text.
Patterns are the shortfall helper's (domain/shortfall.py). Nothing here decides a verdict.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable, Sequence

from .models import PageText, SellerProfile
from .shortfall import detect_documents

UPLOAD_RULES = ("Each file must be a PDF of at most 10 MB and 100 pages. "
                "Merge all the ATC certificates into one PDF.")

_ATC_SLOT = re.compile(r"\(\s*Requested in ATC\s*\)", re.IGNORECASE)


@dataclass(frozen=True)
class ChecklistItem:
    name: str
    source: str            # "bid form" | "atc" | "spec" | "boq"
    page: int | None       # page of the bid PDF, or of the attached file
    quote: str
    in_profile: bool | None
    profile_note: str
    from_atc_slot: bool = False   # the form only says "see the ATC file"
    past_rejection: str | None = None


@dataclass(frozen=True)
class UnreadFile:
    kind: str
    url: str
    note: str


@dataclass
class Checklist:
    items: list[ChecklistItem] = field(default_factory=list)
    unread_files: list[UnreadFile] = field(default_factory=list)
    upload_rules: str = UPLOAD_RULES


def form_entries(value: str) -> list[str]:
    """GeM lists the documents comma-separated; a line break can fall inside an entry."""
    return [" ".join(part.split()) for part in value.split(",") if part.strip()]


def build_checklist(
    form_value: str | None,
    form_page: int | None,
    attached: Sequence[tuple[str, Sequence[PageText]]],  # (kind, pages) of files read as text
    unread: Sequence[UnreadFile],
    profile: SellerProfile | None,
    past_rejections: Callable[[Sequence[str]], list[dict]] = lambda names: [],
) -> Checklist:
    items: dict[str, ChecklistItem] = {}

    def add(item: ChecklistItem) -> None:
        items.setdefault(item.name.lower(), item)

    for entry in form_entries(form_value or ""):
        if _ATC_SLOT.search(entry):
            add(ChecklistItem(re.sub(_ATC_SLOT, "", entry).strip() or "Certificate", "bid form", form_page, entry,
                              None, "The buyer's ATC file says what to attach.", from_atc_slot=True))
            continue
        found = detect_documents(entry, profile)
        if found:
            for doc in found:
                add(ChecklistItem(doc.name, "bid form", form_page, entry, doc.in_profile, doc.profile_note))
        else:
            add(ChecklistItem(entry, "bid form", form_page, entry, None, "Not a standard document: read what the buyer wants."))

    for kind, pages in attached:
        for page in pages:
            for doc in detect_documents(page.text, profile):
                add(ChecklistItem(doc.name, kind, page.number, doc.quote, doc.in_profile, doc.profile_note))

    warnings = past_rejections([item.name for item in items.values()])
    result = []
    for item in items.values():
        note = next((w["warning"] for w in warnings if w["missing_doc"].lower() in item.name.lower()
                     or item.name.lower() in w["missing_doc"].lower()), None)
        result.append(ChecklistItem(**{**item.__dict__, "past_rejection": note}))
    return Checklist(result, list(unread))
