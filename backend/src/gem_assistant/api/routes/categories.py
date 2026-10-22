from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from ...safety.errors import SafetyError

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("")
def categories(q: str, request: Request) -> list[dict]:
    try:
        found = request.app.state.container.categories.lookup(q)
    except ValueError as error:
        raise HTTPException(400, str(error))
    except SafetyError as error:
        raise HTTPException(409, str(error))
    return [{"group": c.group, "name": c.name, "quadrant": c.quadrant, "warning": c.warning} for c in found]
