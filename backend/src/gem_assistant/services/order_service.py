"""Step 1.4: Service for Order Tracker."""

from __future__ import annotations

from typing import Any

from ..domain.models import SellerProfile
from ..domain.order_tracker import (
    TrackedOrder,
    compute_gem_charges,
    compute_order_deadlines,
    draft_payment_delay_incident,
    parse_order_paste,
)
from ..domain.ports import Clock


class OrderService:
    def __init__(self, repo, profiles, clock: Clock):
        self._repo = repo
        self._profiles = profiles
        self._clock = clock

    def save(self, order: TrackedOrder) -> int:
        now = self._clock.now()
        return self._repo.save(order, now)

    def update(self, order_id: int, updates: dict[str, Any]) -> TrackedOrder | None:
        now = self._clock.now()
        if self._repo.update_stage(order_id, updates, now):
            return self._repo.get(order_id)
        return None

    def get(self, order_id: int) -> dict | None:
        order = self._repo.get(order_id)
        if not order:
            return None
        now = self._clock.now()
        cum_sales = self._repo.cumulative_sales()
        return self._decorate(order, now, cum_sales)

    def list(self) -> list[dict]:
        now = self._clock.now()
        cum_sales = self._repo.cumulative_sales()
        return [self._decorate(o, now, cum_sales) for o in self._repo.list()]

    def draft_incident(self, order_id: int) -> str | None:
        order = self._repo.get(order_id)
        if not order:
            return None
        profile = self._profiles.get() or SellerProfile()
        return draft_payment_delay_incident(order, profile)

    def parse_paste(self, text: str) -> TrackedOrder | None:
        return parse_order_paste(text)

    def _decorate(self, order: TrackedOrder, now, cum_sales: int) -> dict:
        deadlines = compute_order_deadlines(order, now)
        charges = compute_gem_charges(order.order_value_rupees, cum_sales)
        return {
            "id": order.id,
            "contract_number": order.contract_number,
            "contract_date": order.contract_date.isoformat(),
            "order_value_rupees": order.order_value_rupees,
            "expected_delivery_date": order.expected_delivery_date.isoformat(),
            "status": order.status.value,
            "epbg_percent": order.epbg_percent,
            "epbg_submitted_at": order.epbg_submitted_at.isoformat() if order.epbg_submitted_at else None,
            "dispatched_at": order.dispatched_at.isoformat() if order.dispatched_at else None,
            "proof_of_delivery_at": order.proof_of_delivery_at.isoformat() if order.proof_of_delivery_at else None,
            "crac_at": order.crac_at.isoformat() if order.crac_at else None,
            "payment_at": order.payment_at.isoformat() if order.payment_at else None,
            "buyer_request_at": order.buyer_request_at.isoformat() if order.buyer_request_at else None,
            "buyer_department": order.buyer_department,
            "deadlines": [
                {
                    "name": d.name,
                    "due_date": d.due_date.isoformat(),
                    "due_text": d.due_text,
                    "is_overdue": d.is_overdue,
                    "severity": d.severity,
                    "action": d.action,
                    "note": d.note,
                    "penalty_rupees": d.penalty_rupees,
                }
                for d in deadlines
            ],
            "charges": {
                "order_value": charges.order_value,
                "milestone_charge": charges.milestone_charge,
                "milestone_gst": charges.milestone_gst,
                "transaction_charge": charges.transaction_charge,
                "transaction_gst": charges.transaction_gst,
                "total_charges": charges.total_charges,
                "tds_applicable": charges.tds_applicable,
            },
        }
