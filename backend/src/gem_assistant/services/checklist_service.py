"""Builds the document checklist of a stored bid (step 2.4).

Reading the attached files costs up to 3 GeM requests, so it only happens when asked
(`read_files=True`) and the answer is kept for this run of the app. The AI reading of the buyer's
terms (`read_terms=True`, step 2.5b) is also only on request; it uses the files when they were read.
"""

from __future__ import annotations

from ..domain.checklist import Checklist, UnreadFile, add_ai_terms, build_checklist
from ..domain.ports import DocumentStore, ProfileReader, TextExtractor
from .atc_reading_service import AtcReadingService
from .attachment_service import Attachment, AttachmentService
from .bid_query_service import BidQueryService
from .rejection_service import RejectionService


class ChecklistService:
    def __init__(self, bids: BidQueryService, documents: DocumentStore, attachments: AttachmentService,
                 profiles: ProfileReader, rejections: RejectionService, extractor: TextExtractor,
                 terms: AtcReadingService):
        self._bids = bids
        self._documents = documents
        self._attachments = attachments
        self._profiles = profiles
        self._rejections = rejections
        self._extractor = extractor
        self._terms = terms
        self._files: dict[int, list[Attachment]] = {}

    def for_bid(self, bid_id: int, read_files: bool = False, read_terms: bool = False) -> Checklist | None:
        item = self._bids.get(bid_id)
        if item is None:
            return None
        bid = item.bid
        if read_files and bid_id not in self._files:
            pdf = self._documents.load(bid.sha256)
            if pdf is not None:  # a safety stop propagates and nothing is cached
                self._files[bid_id] = self._attachments.fetch_for(pdf)
        files = self._files.get(bid_id, [])
        docs = bid.field("documents_required")
        profile = self._profiles.get()
        checklist = build_checklist(
            docs.value if docs else None, docs.evidence.page if docs and docs.evidence else None,
            [(a.kind, a.pages) for a in files if a.status == "read"],
            [UnreadFile(a.kind, a.url, a.note) for a in files if a.status != "read"],
            profile, self._rejections.get_warnings_for_docs)
        if read_terms:
            pdf = self._documents.load(bid.sha256)
            if pdf is not None:
                atc_pages = [p for a in files if a.kind == "atc" and a.status == "read" for p in a.pages]
                checklist = add_ai_terms(checklist, self._terms.read(self._extractor.extract(pdf), atc_pages), profile)
        return checklist
