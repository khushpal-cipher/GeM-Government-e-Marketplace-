"""Step 1.4: Order tracker (HANDOFF §4a, docs/live-tour.md).

Tracks orders through the 4 stages from live GeM screens:
Contract Placed -> Consignment Dispatched -> Consignment Received (CRAC) -> Payment Completed.
Calculates all GeM deadlines, LD penalties, GeM charges, and drafts incident text for delayed payment.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum

from .gem_alerts import _DATE, _REF, MONTHS
from .models import SellerProfile
from .wording import DRAFT_NOTE, IST, day, deadline


class OrderStatus(str, Enum):
    CONTRACT_PLACED = "CONTRACT_PLACED"
    DISPATCHED = "DISPATCHED"
    RECEIVED = "RECEIVED"
    PAYMENT_COMPLETED = "PAYMENT_COMPLETED"


@dataclass(frozen=True)
class GeMCharges:
    order_value: int
    milestone_charge: int
    milestone_gst: int
    transaction_charge: int
    transaction_gst: int
    total_charges: int
    tds_applicable: bool


@dataclass(frozen=True)
class OrderDeadline:
    name: str
    due_date: date
    due_text: str
    is_overdue: bool
    severity: str        # "info", "warn", "bad"
    action: str
    note: str
    penalty_rupees: int = 0


@dataclass
class TrackedOrder:
    contract_number: str
    contract_date: date
    order_value_rupees: int
    expected_delivery_date: date
    id: int | None = None
    epbg_percent: float | None = None
    epbg_submitted_at: date | None = None
    dispatched_at: date | None = None
    proof_of_delivery_at: date | None = None
    crac_at: date | None = None
    payment_at: date | None = None
    buyer_request_at: date | None = None
    buyer_department: str | None = None

    @property
    def status(self) -> OrderStatus:
        if self.payment_at:
            return OrderStatus.PAYMENT_COMPLETED
        if self.crac_at:
            return OrderStatus.RECEIVED
        if self.dispatched_at:
            return OrderStatus.DISPATCHED
        return OrderStatus.CONTRACT_PLACED


def compute_gem_charges(order_value: int, cumulative_sales_rupees: int = 0) -> GeMCharges:
    """Calculates official GeM Revenue Policy v1.5 charges.

    1. Annual Milestone Charge: ₹10,000 + 18% GST once a year when annual sales cross ₹20 lakh.
    2. Transaction Charge: on orders > ₹10 lakh only: 0.30% of order value, capped at ₹3 lakh, + 18% GST.
    3. TDS: 2% applies if total annual charges exceed ₹30,000.
    """
    milestone = 0
    if cumulative_sales_rupees < 2_000_000 and (cumulative_sales_rupees + order_value) >= 2_000_000:
        milestone = 10_000
    milestone_gst = int(round(milestone * 0.18))

    tx = 0
    if order_value > 1_000_000:
        raw_tx = int(round(order_value * 0.0030))
        tx = min(raw_tx, 300_000)
    tx_gst = int(round(tx * 0.18))

    total = milestone + milestone_gst + tx + tx_gst
    tds = total > 30_000

    return GeMCharges(
        order_value=order_value,
        milestone_charge=milestone,
        milestone_gst=milestone_gst,
        transaction_charge=tx,
        transaction_gst=tx_gst,
        total_charges=total,
        tds_applicable=tds,
    )


def compute_order_deadlines(order: TrackedOrder, now: datetime) -> list[OrderDeadline]:
    """Computes deadlines, warnings, and penalties based on GeM GTC v1.29 rules."""
    today = now.astimezone(IST).date() if now.tzinfo else now.date()
    deadlines: list[OrderDeadline] = []

    # 1. ePBG deadline (15 days from contract)
    if order.epbg_percent and order.epbg_percent > 0:
        epbg_due = order.contract_date + timedelta(days=15)
        if not order.epbg_submitted_at:
            overdue = today > epbg_due
            deadlines.append(OrderDeadline(
                name="ePBG Submission",
                due_date=epbg_due,
                due_text=deadline(epbg_due, now),
                is_overdue=overdue,
                severity="bad" if overdue else "warn",
                action="Submit ePBG on GeM within 15 days of contract",
                note="ePBG missing: severe deviation, buyer may cancel order and forfeit EMD",
            ))

    # 2. Invoicing before expected delivery date (expiry warning)
    inv_due = order.expected_delivery_date
    if not order.dispatched_at:
        overdue = today > inv_due
        deadlines.append(OrderDeadline(
            name="Invoice / Delivery Period",
            due_date=inv_due,
            due_text=deadline(inv_due, now),
            is_overdue=overdue,
            severity="bad" if overdue else "warn",
            action="Generate invoice and dispatch goods before expected delivery date",
            note="Order expires and invoice generation is disabled after delivery date.",
        ))

    # 3. Late Delivery (LD) Penalty: 0.5% of value per week (max 5%, or 10% if >25% delay)
    late_ref_date = order.dispatched_at or today
    if late_ref_date > order.expected_delivery_date:
        delay_days = (late_ref_date - order.expected_delivery_date).days
        if delay_days > 0:
            weeks = (delay_days + 6) // 7
            delivery_period_days = max(1, (order.expected_delivery_date - order.contract_date).days)
            max_rate = 0.10 if delay_days > (delivery_period_days * 0.25) else 0.05
            rate = min(weeks * 0.005, max_rate)
            penalty = int(round(order.order_value_rupees * rate))
            deadlines.append(OrderDeadline(
                name="Late Delivery (LD) Penalty",
                due_date=order.expected_delivery_date,
                due_text=deadline(order.expected_delivery_date, now),
                is_overdue=True,
                severity="bad",
                action="Deliver remaining items; LD will be deducted by buyer",
                note=f"0.5% per week late (delayed by {delay_days} days = {weeks} week{'s' if weeks > 1 else ''}). Max cap {int(max_rate * 100)}%.",
                penalty_rupees=penalty,
            ))

    # 4. Buyer Request (5 days to respond)
    if order.buyer_request_at:
        req_due = order.buyer_request_at + timedelta(days=5)
        overdue = today > req_due
        deadlines.append(OrderDeadline(
            name="Buyer Request Response",
            due_date=req_due,
            due_text=deadline(req_due, now),
            is_overdue=overdue,
            severity="bad" if overdue else "warn",
            action="Accept or decline buyer request on GeM",
            note="5 calendar days to respond; no reply = automatically declined and invoicing stays blocked.",
        ))

    # 5. CRAC issuance (10 days after proof of delivery)
    if order.proof_of_delivery_at and not order.crac_at:
        crac_due = order.proof_of_delivery_at + timedelta(days=10)
        overdue = today > crac_due
        deadlines.append(OrderDeadline(
            name="CRAC Generation",
            due_date=crac_due,
            due_text=deadline(crac_due, now),
            is_overdue=overdue,
            severity="bad" if overdue else "info",
            action="Follow up with consignee for CRAC or wait for auto-CRAC",
            note="Consignee must issue CRAC within 10 days of delivery proof; raise 'delay in CRAC' incident if pending.",
        ))

    # 6. Payment (due 10 days after CRAC)
    if order.crac_at and not order.payment_at:
        pay_due = order.crac_at + timedelta(days=10)
        overdue = today > pay_due
        deadlines.append(OrderDeadline(
            name="Payment Due",
            due_date=pay_due,
            due_text=deadline(pay_due, now),
            is_overdue=overdue,
            severity="bad" if overdue else "info",
            action="Raise 'delay in payment' incident on GeM" if overdue else "Follow up for payment",
            note=f"Payment due 10 days after CRAC.{' Late payment: buyer owes 1% interest per month.' if overdue else ''}",
        ))

    return deadlines


def draft_payment_delay_incident(order: TrackedOrder, profile: SellerProfile | None = None) -> str:
    """Drafts covering text for 'delay in payment' incident following 1.0 wording rules."""
    profile = profile or SellerProfile()
    firm_name = profile.business_name.strip() if profile.business_name else "[your firm name]"
    crac_str = day(order.crac_at) if order.crac_at else "[CRAC date]"
    contract_date_str = day(order.contract_date)
    pay_due = order.crac_at + timedelta(days=10) if order.crac_at else None
    due_str = day(pay_due) if pay_due else "[due date]"
    dept_str = f" issued by {order.buyer_department}" if order.buyer_department else ""

    draft = (
        f"{DRAFT_NOTE}\n\n"
        f"To: Competent Authority, Incident Management, GeM\n"
        f"Subject: Incident - Delay in payment against Contract {order.contract_number}\n\n"
        f"Dear Sir/Madam,\n\n"
        f"We draw your attention to Contract {order.contract_number} dated {contract_date_str} "
        f"for an order value of Rs {order.order_value_rupees:,}{dept_str}.\n\n"
        f"The consignment was delivered and the Consignee Receipt and Acceptance Certificate (CRAC) "
        f"was issued on {crac_str}.\n\n"
        f"Under GeM General Terms and Conditions (GTC) Clause 12, payment is due within 10 days of CRAC "
        f"generation, which was due on {due_str}. To date, the payment remains pending.\n\n"
        f"We request your urgent intervention to arrange the release of the overdue payment. "
        f"Per GeM guidelines, delayed payments attract interest at 1% per month.\n\n"
        f"Yours faithfully,\n"
        f"{firm_name}"
    )
    return draft


def _parse_first_date(text: str) -> date | None:
    for m in _DATE.finditer(text):
        try:
            if m.group("y2"):
                return date(int(m.group("y2")), int(m.group("m2")), int(m.group("d2")))
            month = int(m.group("m")) if m.group("m") else MONTHS.get(m.group("mon").lower())
            if month:
                return date(int(m.group("y")), month, int(m.group("d")))
        except ValueError:
            continue
    return None


def parse_order_paste(text: str) -> TrackedOrder | None:
    """Extracts contract details from text pasted from the GeM Orders screen."""
    ref_match = _REF.search(text)
    if not ref_match:
        return None
    contract_number = ref_match.group(0).upper()

    # Dates
    dates = []
    for m in _DATE.finditer(text):
        try:
            if m.group("y2"):
                dates.append((m.start(), date(int(m.group("y2")), int(m.group("m2")), int(m.group("d2")))))
            else:
                month = int(m.group("m")) if m.group("m") else MONTHS.get(m.group("mon").lower())
                if month:
                    dates.append((m.start(), date(int(m.group("y")), month, int(m.group("d")))))
        except ValueError:
            continue

    contract_date = dates[0][1] if dates else date.today()
    expected_delivery_date = dates[1][1] if len(dates) > 1 else contract_date + timedelta(days=15)

    # Order value: look for numbers with currency or commas
    val_match = re.search(r"(?:INR|Rs\.?|₹|Value[:\s]+(?:INR|Rs\.?)?)\s*([0-9,]+(?:\.[0-9]{2})?)", text, re.IGNORECASE)
    if val_match:
        clean_val = val_match.group(1).replace(",", "").split(".")[0]
        order_value = int(clean_val)
    else:
        order_value = 0

    # ePBG percent
    epbg_match = re.search(r"ePBG[:\s]+(\d+(?:\.\d+)?)\s*%", text, re.IGNORECASE)
    epbg_percent = float(epbg_match.group(1)) if epbg_match else None

    # Buyer department
    dept_match = re.search(r"Department[:\s]+([^\n\r,]+)", text, re.IGNORECASE)
    buyer_department = dept_match.group(1).strip() if dept_match else None

    return TrackedOrder(
        contract_number=contract_number,
        contract_date=contract_date,
        order_value_rupees=order_value,
        expected_delivery_date=expected_delivery_date,
        epbg_percent=epbg_percent,
        buyer_department=buyer_department,
    )
