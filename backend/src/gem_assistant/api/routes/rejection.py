"""Step 1.5: API routes for Rejection reason reader + challenge draft."""

from __future__ import annotations

from datetime import date
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

router = APIRouter(prefix="/api/rejection", tags=["rejection"])


class AnalyzeIn(BaseModel):
    text: str
    bid_number: str | None = None
    eval_date: str | None = None


class SaveRejectionIn(BaseModel):
    bid_number: str | None = None
    reason_text: str
    missing_doc: str | None = None
    category: str | None = None


@router.post("/analyze")
def analyze(body: AnalyzeIn, request: Request) -> dict[str, Any]:
    container = request.app.state.container
    eval_date = None
    if body.eval_date:
        try:
            eval_date = date.fromisoformat(body.eval_date)
        except ValueError:
            pass

    analysis = container.rejection_service.analyze(
        text=body.text,
        bid_number=body.bid_number,
        eval_date=eval_date,
    )

    return {
        "bid_number": analysis.bid_number,
        "raw_text": analysis.raw_text,
        "evaluation_date": analysis.evaluation_date.isoformat() if analysis.evaluation_date else None,
        "challenge_deadline_date": analysis.challenge_deadline_date.isoformat() if analysis.challenge_deadline_date else None,
        "deadline_text": analysis.deadline_text,
        "primary_reason": analysis.primary_reason,
        "summary": analysis.summary,
        "emd_involved": analysis.emd_involved,
        "technical_deviation": analysis.technical_deviation,
        "has_rebuttal": analysis.has_rebuttal,
        "rebuttal_points": analysis.rebuttal_points,
        "missing_docs": [
            {
                "name": d.name,
                "quote": d.quote,
                "in_profile": d.in_profile,
                "profile_note": d.profile_note,
                "placeholder": d.placeholder,
            }
            for d in analysis.missing_docs
        ],
        "challenge_draft": analysis.challenge_draft,
    }


@router.post("/history")
def save_history(body: SaveRejectionIn, request: Request) -> dict[str, Any]:
    container = request.app.state.container
    rec_id = container.rejection_service.save_rejection(
        bid_number=body.bid_number,
        reason_text=body.reason_text,
        missing_doc=body.missing_doc,
        category=body.category,
    )
    return {"id": rec_id}


@router.get("/history")
def list_history(request: Request) -> dict[str, Any]:
    container = request.app.state.container
    items = container.rejection_service.list_history()
    return {"items": items}


@router.delete("/history/{rejection_id}")
def delete_history(rejection_id: int, request: Request) -> dict[str, Any]:
    container = request.app.state.container
    success = container.rejection_service.delete_history_item(rejection_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rejection history entry not found")
    return {"success": True}


@router.get("/warnings")
def check_warnings(docs: str = "", request: Request = None) -> dict[str, Any]:
    container = request.app.state.container
    doc_list = [d.strip() for d in docs.split(",") if d.strip()]
    warnings = container.rejection_service.get_warnings_for_docs(doc_list)
    return {"warnings": warnings}
