from __future__ import annotations

from dataclasses import asdict
from typing import Literal

from fastapi import APIRouter, HTTPException, Request, UploadFile
from pydantic import BaseModel

from ...domain.models import item_match, matching_items
from ...infrastructure.pypdf_extractor import InvalidPdf
from ...safety.errors import SafetyError, UnexpectedResponse, UrlNotAllowed
from ...services.bid_fetch_service import BadBidLink
from ...services.bid_import_service import EvidenceMismatch
from ..schemas import BidDetailOut, BidSummaryOut, FetchIn, FetchOut, ImportOut

router = APIRouter(prefix="/api/bids", tags=["bids"])


@router.get("", response_model=list[BidSummaryOut])
def list_bids(request: Request) -> list[BidSummaryOut]:
    return [BidSummaryOut.from_assessed(b) for b in request.app.state.container.bid_query.list()]


@router.get("/{bid_id}", response_model=BidDetailOut)
def get_bid(bid_id: int, request: Request) -> BidDetailOut:
    item = request.app.state.container.bid_query.get(bid_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Bid not found")
    container = request.app.state.container
    profile = container.profiles.get()
    text = item.bid.found_value("item_category")
    return BidDetailOut.from_assessed(item).model_copy(update={
        "buyer_flag": container.buyer_flags.get(bid_id),
        "your_items": matching_items(text, profile.categories, profile.ignore_words) if profile else [],
        "item_count": item_match(text, [])[1]})


@router.get("/{bid_id}/past-prices")
def past_prices(bid_id: int, request: Request) -> list[dict]:
    """For each item of this bid: what similar items won for before (from result pages already kept)."""
    container = request.app.state.container
    item = container.bid_query.get(bid_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Bid not found")
    names = [i.strip() for i in (item.bid.found_value("item_category") or "").split(",") if i.strip()]
    return [container.past_prices.similar(n) for n in names[:10]]


@router.get("/{bid_id}/representation")
def representation(bid_id: int, request: Request) -> dict:
    result = request.app.state.container.representations.draft(bid_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Bid not found")
    return result


class BuyerFlagIn(BaseModel):
    flag: Literal["none", "orange", "red", "unknown"]  # "unknown" clears the note


@router.put("/{bid_id}/buyer-flag")
def set_buyer_flag(bid_id: int, body: BuyerFlagIn, request: Request) -> dict:
    """The buyer's payment flag as he read it on GeM's bid page. GeM shows it only to a logged-in seller,
    so the app never fetches it."""
    container = request.app.state.container
    if container.bid_query.get(bid_id) is None:
        raise HTTPException(status_code=404, detail="Bid not found")
    flag = None if body.flag == "unknown" else body.flag
    container.buyer_flags.set(bid_id, flag, container.clock.now())
    return {"buyer_flag": flag}


class ChecklistIn(BaseModel):
    read_files: bool = False
    read_terms: bool = False  # the AI reads the buyer's terms (one Groq call, cached)


@router.post("/{bid_id}/checklist")
def bid_checklist(bid_id: int, body: ChecklistIn, request: Request) -> dict:
    """Documents this bid asks for. `read_files` also downloads the files the bid links to (<= 3 requests)."""
    try:
        checklist = request.app.state.container.checklists.for_bid(bid_id, body.read_files, body.read_terms)
    except SafetyError as error:  # breaker open, blocked, budget used up
        raise HTTPException(status_code=409, detail=str(error)) from error
    if checklist is None:
        raise HTTPException(status_code=404, detail="Bid not found")
    return asdict(checklist)


@router.post("/import", response_model=ImportOut)
async def import_bid(file: UploadFile, request: Request) -> ImportOut:
    container = request.app.state.container
    limit = container.settings.safety.max_download_bytes
    data = await file.read(limit + 1)
    try:
        result = container.bid_import.import_pdf(data, source_name=file.filename or "upload.pdf")
    except (InvalidPdf, ValueError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return ImportOut(id=result.id, already_imported=result.already_imported)


@router.post("/fetch", response_model=FetchOut)
def fetch_bid(body: FetchIn, request: Request) -> FetchOut:
    """Download one bid document from GeM by its link, through the safety layer."""
    service = request.app.state.container.bid_fetch
    try:
        result = service.fetch_from_link(body.link)
    except (BadBidLink, UrlNotAllowed) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except UnexpectedResponse as error:
        raise HTTPException(status_code=404, detail=f"GeM didn't return a usable document ({error}).") from error
    except SafetyError as error:  # breaker open, blocked, budget used up
        raise HTTPException(status_code=409, detail=str(error)) from error
    except (InvalidPdf, EvidenceMismatch) as error:
        raise HTTPException(status_code=422, detail=f"Downloaded, but could not analyse it: {error}") from error
    except Exception as error:  # network trouble; logged by the safety layer, not retried
        raise HTTPException(status_code=502, detail=f"Could not reach GeM: {type(error).__name__}") from error
    return FetchOut(id=result.import_result.id, already_imported=result.import_result.already_imported,
                    downloaded=result.downloaded)


class InvitedPasteIn(BaseModel):
    text: str


class InvitedImportIn(BaseModel):
    bid_numbers: list[str]


@router.post("/invited/parse")
def parse_invited(body: InvitedPasteIn, request: Request) -> dict:
    return {"items": request.app.state.container.invited_bids.parse(body.text)}


@router.post("/invited/import")
def import_invited(body: InvitedImportIn, request: Request) -> dict:
    try:
        return {"items": request.app.state.container.invited_bids.import_bids(body.bid_numbers)}
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
