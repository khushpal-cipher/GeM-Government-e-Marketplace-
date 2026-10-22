from __future__ import annotations

from fastapi import APIRouter, Request, Response

router = APIRouter(prefix="/api/export", tags=["export"])


def _file(text: str, name: str) -> Response:
    return Response(text, media_type="text/csv; charset=utf-8",
                    headers={"Content-Disposition": f'attachment; filename="{name}"'})


@router.get("/bids.csv")
def bids_csv(request: Request) -> Response:
    return _file(request.app.state.container.export.bids_csv(), "gem-bids.csv")


@router.get("/orders.csv")
def orders_csv(request: Request) -> Response:
    return _file(request.app.state.container.export.orders_csv(), "gem-orders.csv")
