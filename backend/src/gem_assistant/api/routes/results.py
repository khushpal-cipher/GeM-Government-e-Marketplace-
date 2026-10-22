from __future__ import annotations

from decimal import Decimal, InvalidOperation

from fastapi import APIRouter, HTTPException, Request

from ...safety.errors import SafetyError
from ...services.result_service import ResultLimitReached

router = APIRouter(prefix="/api/results", tags=["results"])


@router.get("/similar")
def similar(item: str, request: Request) -> dict:
    return request.app.state.container.past_prices.similar(item)


@router.get("/{doc_id}")
def result(doc_id: str, request: Request, packets: str = "") -> dict:
    try:
        return request.app.state.container.results.read(doc_id, packets)
    except ValueError as error:
        raise HTTPException(400, str(error))
    except (SafetyError, ResultLimitReached) as error:
        raise HTTPException(409, str(error))


@router.get("/direct-order/check")
def direct_order(link: str, target_price: str, request: Request) -> dict:
    try:
        return request.app.state.container.direct_order.check(link, Decimal(target_price))
    except InvalidOperation:
        raise HTTPException(400, "The price must be a number.")
    except ValueError as error:
        raise HTTPException(400, str(error))
    except SafetyError as error:
        raise HTTPException(409, str(error))
