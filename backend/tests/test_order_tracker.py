"""Step 1.4: Order tracker.

Tracks orders through the 4 stages from live tour:
Contract Placed -> Dispatched -> Received (CRAC) -> Payment.
Deadlines from HANDOFF §4a:
- ePBG within 15 days
- Invoicing before expected delivery date (expiry warning)
- LD penalty 0.5%/week late (max 5% or 10% if delay > 25% of delivery time)
- Buyer request within 5 days
- CRAC within 10 days of delivery proof
- Payment within 10 days of CRAC -> "delay in payment" incident draft
- GeM charges calculator (milestone ₹10k+GST at ₹20L, 0.30% capped at ₹3L on orders > ₹10L).
"""

from __future__ import annotations

from datetime import date, datetime, timezone

import pytest
from fastapi.testclient import TestClient

from gem_assistant.api.app import create_app
from gem_assistant.domain.models import SellerProfile
from gem_assistant.domain.order_tracker import (
    OrderStatus,
    TrackedOrder,
    compute_gem_charges,
    compute_order_deadlines,
    draft_payment_delay_incident,
    parse_order_paste,
)
from gem_assistant.domain.wording import DRAFT_NOTE, check_draft

NOW = datetime(2026, 10, 20, 6, 30, tzinfo=timezone.utc)  # Tue 20 Oct 2026, 12:00 PM IST
TODAY = date(2026, 10, 20)


# ---------- GeM Charges Calculator ----------

@pytest.mark.parametrize("order_val, cum_sales, exp_milestone, exp_tx, exp_total", [
    # Order <= 10L, cum sales < 20L: no milestone, no tx charge
    (500_000, 500_000, 0, 0, 0),
    # Order <= 10L, crosses 20L: milestone ₹10,000 + 18% GST = ₹11,800, no tx charge
    (800_000, 1_500_000, 10_000, 0, 11_800),
    # Order 15L (> 10L): 0.30% = ₹4,500 + 18% GST = ₹5,310; cum sales already > 20L
    (1_500_000, 2_500_000, 0, 4_500, 5_310),
    # Order 25L: crosses 20L (milestone 11,800) + 0.30% of 25L = 7,500 + 18% GST (8,850) = 20,650
    (2_500_000, 0, 10_000, 7_500, 20_650),
    # Max cap check: ₹15 crore order -> 0.30% is 4.5 lakh, capped at 3 lakh + 18% GST (3.54 lakh)
    (150_000_000, 30_000_000, 0, 300_000, 354_000),
])
def test_gem_charges_calculator(order_val, cum_sales, exp_milestone, exp_tx, exp_total):
    charges = compute_gem_charges(order_val, cum_sales)
    assert charges.milestone_charge == exp_milestone
    assert charges.transaction_charge == exp_tx
    assert charges.total_charges == exp_total


# ---------- Deadlines & Status ----------

def test_order_stages_progression():
    # 1. Placed
    o1 = TrackedOrder(
        contract_number="GEMC-511687724", contract_date=date(2026, 10, 1),
        order_value_rupees=1_500_000, expected_delivery_date=date(2026, 10, 25))
    assert o1.status == OrderStatus.CONTRACT_PLACED

    # 2. Dispatched
    o2 = TrackedOrder(
        contract_number="GEMC-511687724", contract_date=date(2026, 10, 1),
        order_value_rupees=1_500_000, expected_delivery_date=date(2026, 10, 25),
        dispatched_at=date(2026, 10, 10))
    assert o2.status == OrderStatus.DISPATCHED

    # 3. Received
    o3 = TrackedOrder(
        contract_number="GEMC-511687724", contract_date=date(2026, 10, 1),
        order_value_rupees=1_500_000, expected_delivery_date=date(2026, 10, 25),
        dispatched_at=date(2026, 10, 10), crac_at=date(2026, 10, 15))
    assert o3.status == OrderStatus.RECEIVED

    # 4. Paid
    o4 = TrackedOrder(
        contract_number="GEMC-511687724", contract_date=date(2026, 10, 1),
        order_value_rupees=1_500_000, expected_delivery_date=date(2026, 10, 25),
        dispatched_at=date(2026, 10, 10), crac_at=date(2026, 10, 15), payment_at=date(2026, 10, 18))
    assert o4.status == OrderStatus.PAYMENT_COMPLETED


def test_epbg_deadline_15_days():
    # Contract 10 Oct, ePBG 3% -> due 25 Oct (15 days)
    order = TrackedOrder(
        contract_number="GEMC-1", contract_date=date(2026, 10, 10),
        order_value_rupees=1_000_000, expected_delivery_date=date(2026, 11, 10),
        epbg_percent=3.0)
    deadlines = compute_order_deadlines(order, NOW)
    epbg = next(d for d in deadlines if "ePBG" in d.name)
    assert epbg.due_date == date(2026, 10, 25)
    assert not epbg.is_overdue

    # Past 15 days without submission: overdue
    old_order = TrackedOrder(
        contract_number="GEMC-2", contract_date=date(2026, 10, 1),
        order_value_rupees=1_000_000, expected_delivery_date=date(2026, 11, 10),
        epbg_percent=3.0)
    d_old = compute_order_deadlines(old_order, NOW)
    epbg_old = next(d for d in d_old if "ePBG" in d.name)
    assert epbg_old.is_overdue
    assert "missed" in epbg_old.due_text


def test_invoice_expiry_warning_before_expected_delivery():
    order = TrackedOrder(
        contract_number="GEMC-1", contract_date=date(2026, 10, 1),
        order_value_rupees=500_000, expected_delivery_date=date(2026, 10, 22))
    deadlines = compute_order_deadlines(order, NOW)
    inv = next(d for d in deadlines if "Invoice" in d.name or "Delivery" in d.name)
    assert inv.due_date == date(2026, 10, 22)
    assert "expire" in inv.note.lower()


def test_late_delivery_penalty_calculation():
    # Delivery date was 10 Oct 2026, contract placed 1 Oct (delivery period = 9 days).
    # Dispatched on 20 Oct 2026 (delay of 10 days = 2 weeks).
    # Delay 10 days > 25% of 9 days (2.25 days) -> max cap is 10%.
    # 2 weeks @ 0.5%/week = 1.0% of ₹10,00,000 = ₹10,000.
    order = TrackedOrder(
        contract_number="GEMC-1", contract_date=date(2026, 10, 1),
        order_value_rupees=1_000_000, expected_delivery_date=date(2026, 10, 10),
        dispatched_at=date(2026, 10, 20))
    deadlines = compute_order_deadlines(order, NOW)
    ld = next(d for d in deadlines if "Late Delivery" in d.name)
    assert ld.penalty_rupees == 10_000


def test_buyer_request_deadline_5_days():
    order = TrackedOrder(
        contract_number="GEMC-1", contract_date=date(2026, 10, 1),
        order_value_rupees=500_000, expected_delivery_date=date(2026, 10, 25),
        buyer_request_at=date(2026, 10, 18))
    deadlines = compute_order_deadlines(order, NOW)
    req = next(d for d in deadlines if "Buyer Request" in d.name)
    assert req.due_date == date(2026, 10, 23)  # 18 + 5 days
    assert not req.is_overdue


def test_crac_deadline_10_days_after_pod():
    order = TrackedOrder(
        contract_number="GEMC-1", contract_date=date(2026, 10, 1),
        order_value_rupees=500_000, expected_delivery_date=date(2026, 10, 25),
        dispatched_at=date(2026, 10, 5), proof_of_delivery_at=date(2026, 10, 8))
    deadlines = compute_order_deadlines(order, NOW)
    crac = next(d for d in deadlines if "CRAC" in d.name)
    assert crac.due_date == date(2026, 10, 18)  # 8 + 10 days
    assert crac.is_overdue


def test_payment_deadline_10_days_after_crac_and_incident_draft():
    # CRAC generated on 5 Oct 2026 -> payment due 15 Oct 2026.
    # Today is 20 Oct 2026 -> late by 5 days.
    order = TrackedOrder(
        contract_number="GEMC-511687724", contract_date=date(2026, 9, 20),
        order_value_rupees=1_500_000, expected_delivery_date=date(2026, 10, 1),
        dispatched_at=date(2026, 9, 25), crac_at=date(2026, 10, 5),
        buyer_department="Ministry of Education")
    deadlines = compute_order_deadlines(order, NOW)
    pay = next(d for d in deadlines if "Payment" in d.name)
    assert pay.due_date == date(2026, 10, 15)
    assert pay.is_overdue
    assert "1% interest" in pay.note

    # Draft covering text for incident
    profile = SellerProfile(business_name="Apex Supplies")
    draft = draft_payment_delay_incident(order, profile)
    assert draft.startswith(DRAFT_NOTE)
    assert "GEMC-511687724" in draft
    assert "Apex Supplies" in draft
    assert "15 Oct 2026" in draft
    assert check_draft(draft) == []


# ---------- Paste Parsing ----------

SAMPLE_ORDER_PASTE = """Contract Details
Contract No: GEMC-511687724
Contract Date: 05-10-2026
Total Value: INR 12,50,000.00
Expected Delivery Date: 25-10-2026
ePBG: 3.0%
Department: Department of Health"""


def test_parse_order_paste():
    order = parse_order_paste(SAMPLE_ORDER_PASTE)
    assert order is not None
    assert order.contract_number == "GEMC-511687724"
    assert order.contract_date == date(2026, 10, 5)
    assert order.order_value_rupees == 1_250_000
    assert order.expected_delivery_date == date(2026, 10, 25)
    assert order.epbg_percent == 3.0
    assert order.buyer_department == "Department of Health"


# ---------- API Endpoints ----------

@pytest.fixture
def client(container):
    return TestClient(create_app(container, allowed_hosts=frozenset({"testserver"})))


def test_order_api_lifecycle(client):
    # Save order
    res = client.post("/api/orders", json={
        "contract_number": "GEMC-998877",
        "contract_date": "2026-10-01",
        "order_value_rupees": 1500000,
        "expected_delivery_date": "2026-10-25",
        "epbg_percent": 3.0,
        "buyer_department": "Railways",
    })
    assert res.status_code == 200

    # List orders
    orders = client.get("/api/orders").json()
    assert len(orders) >= 1
    saved = next(o for o in orders if o["contract_number"] == "GEMC-998877")
    assert saved["order_value_rupees"] == 1500000
    assert saved["status"] == "CONTRACT_PLACED"
    assert len(saved["deadlines"]) >= 1
    assert saved["charges"]["total_charges"] > 0

    # Update order stage (e.g. CRAC)
    update_res = client.put(f"/api/orders/{saved['id']}", json={
        "crac_at": "2026-10-10"
    })
    assert update_res.status_code == 200
    updated = update_res.json()
    assert updated["status"] == "RECEIVED"

    # Incident draft endpoint
    incident_res = client.get(f"/api/orders/{saved['id']}/incident-draft")
    assert incident_res.status_code == 200
    assert incident_res.json()["draft"].startswith(DRAFT_NOTE)
