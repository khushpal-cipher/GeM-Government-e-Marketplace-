"""CSV for Excel (step 5.3): his bids with verdicts and checklist, and his orders. Read-only."""

from __future__ import annotations

import csv
import io

BOM = "﻿"  # makes Excel read the file as UTF-8 (₹, names)


def _safe(value) -> str:
    """Buyer-written text must not run as a formula when the file is opened in a spreadsheet."""
    text = "" if value is None else str(value)
    return "'" + text if text[:1] in ("=", "+", "-", "@", "\t", "\r") else text


def _csv(header: list[str], rows: list[list]) -> str:
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(header)
    writer.writerows([_safe(c) for c in row] for row in rows)
    return BOM + out.getvalue()


class ExportService:
    def __init__(self, bid_query, checklists, orders):
        self._bids, self._checklists, self._orders = bid_query, checklists, orders

    def bids_csv(self) -> str:
        rows = []
        for item in self._bids.list():
            bid = item.bid
            checklist = self._checklists.for_bid(bid.id)  # form only: reading attached files costs GeM requests
            end = bid.deadline()
            rows.append([
                bid.bid_number, bid.found_value("item_category"),
                bid.found_value("organisation") or bid.found_value("ministry"),
                end.isoformat() if end else "", item.assessment.verdict.value,
                " | ".join(r.reason for r in item.assessment.results if r.outcome.value != "ELIGIBLE"),
                " | ".join(i.name for i in checklist.items) if checklist else "",
            ])
        return _csv(["Bid number", "Items", "Buyer", "Closes", "Verdict", "Things to check", "Documents to prepare"], rows)

    def orders_csv(self) -> str:
        rows = [[o["contract_number"], o["contract_date"], o["order_value_rupees"], o["expected_delivery_date"],
                 o["status"], o["buyer_department"],
                 " | ".join(f"{d['name']}: {d['due_text']}" for d in o["deadlines"])] for o in self._orders.list()]
        return _csv(["Contract", "Date", "Value (Rs)", "Expected delivery", "Status", "Buyer", "Next dates"], rows)
