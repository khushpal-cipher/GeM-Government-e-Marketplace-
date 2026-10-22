"""Builds the document checklist of a stored bid (step 2.4).

Reading the attached files costs up to 3 GeM requests, so it only happens when asked
(`read_files=True`) and the answer is kept for this run of the app.
"""

from __future__ import annotations

from ..domain.checklist import Checklist, UnreadFile, build_checklist
from ..domain.ports import DocumentStore, ProfileReader
from .attachment_service import Attachment, AttachmentService
from .bid_query_service import BidQueryService
from .rejection_service import RejectionService


class ChecklistService:
    def __init__(self, bids: BidQueryService, documents: DocumentStore, attachments: AttachmentService,
                 profiles: ProfileReader, rejections: RejectionService):
        self._bids = bids
        self._documents = documents
        self._attachments = attachments
        self._profiles = profiles
        self._rejections = rejections
        self._files: dict[int, list[Attachment]] = {}

    def for_bid(self, bid_id: int, read_files: bool = False) -> Checklist | None:
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
        return build_checklist(
            docs.value if docs else None, docs.evidence.page if docs and docs.evidence else None,
            [(a.kind, a.pages) for a in files if a.status == "read"],
            [UnreadFile(a.kind, a.url, a.note) for a in files if a.status != "read"],
            self._profiles.get(), self._rejections.get_warnings_for_docs)
