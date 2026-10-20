from __future__ import annotations

from datetime import date
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

router = APIRouter(prefix="/api/orders", tags=["orders"])


class OrderIn(BaseModel):
    contract_number: str
    contract_date: date
    order_value_rupees: int
    expected_delivery_date: date
    epbg_percent: float | None = None
    buyer_department: str | None = None


class OrderUpdateIn(BaseModel):
    epbg_submitted_at: date | None = None
    dispatched_at: date | None = None
    proof_of_delivery_at: date | None = None
    crac_at: date | None = None
    payment_at: date | None = None
    buyer_request_at: date | None = None
    buyer_department: str | None = None


class PasteIn(BaseModel):
    text: str


@router.post("/parse")
def parse_paste(body: PasteIn, request: Request) -> dict:
    order = request.app.state.container.orders.parse_paste(body.text)
    if not order:
        raise HTTPException(status_code=422, detail="No contract number found in the pasted text.")
    return {
        "contract_number": order.contract_number,
        "contract_date": order.contract_date.isoformat(),
        "order_value_rupees": order.order_value_rupees,
        "expected_delivery_date": order.expected_delivery_date.isoformat(),
        "epbg_percent": order.epbg_percent,
        "buyer_department": order.buyer_department,
    }


@router.post("")
def save_order(body: OrderIn, request: Request) -> dict:
    from ...domain.order_tracker import TrackedOrder
    order = TrackedOrder(
        contract_number=body.contract_number,
        contract_date=body.contract_date,
        order_value_rupees=body.order_value_rupees,
        expected_delivery_date=body.expected_delivery_date,
        epbg_percent=body.epbg_percent,
        buyer_department=body.buyer_department,
    )
    order_id = request.app.state.container.orders.save(order)
    result = request.app.state.container.orders.get(order_id)
    return result


@router.get("")
def list_orders(request: Request) -> list[dict]:
    return request.app.state.container.orders.list()


@router.get("/{order_id}")
def get_order(order_id: int, request: Request) -> dict:
    result = request.app.state.container.orders.get(order_id)
    if result is None:
        raise HTTPException(status_code=404, detail="No such order")
    return result


@router.put("/{order_id}")
def update_order(order_id: int, body: OrderUpdateIn, request: Request) -> dict:
    updates = {k: v for k, v in body.model_dump().items() if v is not None}
    result = request.app.state.container.orders.update(order_id, updates)
    if result is None:
        raise HTTPException(status_code=404, detail="No such order")
    return request.app.state.container.orders.get(order_id)


@router.get("/{order_id}/incident-draft")
def incident_draft(order_id: int, request: Request) -> dict:
    draft = request.app.state.container.orders.draft_incident(order_id)
    if draft is None:
        raise HTTPException(status_code=404, detail="No such order")
    return {"draft": draft}
