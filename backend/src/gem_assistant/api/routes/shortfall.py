from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter(prefix="/api/shortfall", tags=["shortfall"])


class ShortfallIn(BaseModel):
    text: str
    bid_number: str | None = None
    due: date | None = None


@router.post("/reply")
def shortfall_reply(body: ShortfallIn, request: Request) -> dict:
    reply = request.app.state.container.shortfall.reply(
        text=body.text, bid_number=body.bid_number, due=body.due
    )
    return {
        "bid_number": reply.bid_number,
        "due": reply.due.isoformat() if reply.due else None,
        "due_text": reply.due_text,
        "documents": [
            {
                "name": d.name,
                "quote": d.quote,
                "in_profile": d.in_profile,
                "profile_note": d.profile_note,
                "placeholder": d.placeholder,
            }
            for d in reply.documents
        ],
        "draft": reply.draft,
        "clarification_text": reply.clarification_text,
    }
