from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from ...safety.errors import SafetyError
from ...services.result_service import ResultLimitReached

router = APIRouter(prefix="/api/results", tags=["results"])


@router.get("/{doc_id}")
def result(doc_id: str, request: Request, packets: str = "") -> dict:
    try:
        return request.app.state.container.results.read(doc_id, packets)
    except ValueError as error:
        raise HTTPException(400, str(error))
    except (SafetyError, ResultLimitReached) as error:
        raise HTTPException(409, str(error))
