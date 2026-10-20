from __future__ import annotations

from datetime import date
from typing import Literal

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from ...domain.gem_alerts import KINDS

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

Kind = Literal["clarification", "acceptance", "delivery", "payment", "scn"]


class PasteIn(BaseModel):
    kind: Kind
    text: str


class ItemIn(BaseModel):
    ref: str = ""
    text: str
    due: date | None = None


class SaveIn(BaseModel):
    kind: Kind
    items: list[ItemIn]


@router.get("/kinds")
def kinds() -> dict:
    return {k: {"label": v.label, "ask": v.ask} for k, v in KINDS.items()}


@router.post("/preview")
def preview(body: PasteIn, request: Request) -> list[dict]:
    drafts = request.app.state.container.alerts.preview(body.kind, body.text)
    return [{"ref": d.ref, "text": d.text, "due": d.due.isoformat() if d.due else None,
             "unclear": d.unclear} for d in drafts]


@router.post("")
def save(body: SaveIn, request: Request) -> dict:
    items = [{"ref": i.ref, "text": i.text, "due": i.due.isoformat() if i.due else None} for i in body.items]
    return {"added": request.app.state.container.alerts.add(body.kind, items)}


@router.get("")
def open_alerts(request: Request) -> list[dict]:
    return request.app.state.container.alerts.open()


@router.post("/{alert_id}/done")
def done(alert_id: int, request: Request) -> dict:
    if not request.app.state.container.alerts.done(alert_id):
        raise HTTPException(status_code=404, detail="No such open alert")
    return {"done": True}
