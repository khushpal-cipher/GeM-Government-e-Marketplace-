"""Downloads the files a bid PDF itself links to: the buyer's ATC file, the specification
PDF and the BOQ document (docs/02-RECON-FINDINGS.md §7, §10).

Only links read from the bid PDF are fetched, only the host/path shapes below, never
`/resources/`. Every request goes through SafeFetcher. Text PDFs are read; a scanned
file or a non-PDF is reported as "open it yourself". A safety stop propagates.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from typing import Callable

from ..domain.models import PageText
from ..domain.ports import DocumentStore, TextExtractor
from ..infrastructure.pypdf_extractor import InvalidPdf, PdfLink, pdf_links
from ..safety.errors import UnexpectedResponse
from ..safety.response_classifier import Expect
from ..safety.safe_fetcher import SafeFetcher

MAX_FILES_PER_BID = 3
MAX_PAGES = 100

# In reading order: the buyer's own terms first.
ATTACHMENT_KINDS = (
    ("atc", re.compile(r"^https://fulfilment\.gem\.gov\.in/contract/slafds\?")),
    ("spec", re.compile(r"^https://mkp\.gem\.gov\.in/catalog_data/.*SpecificationDocument/")),
    ("boq", re.compile(r"^https://mkp\.gem\.gov\.in/uploaded_documents/.*/OrderItem/BoqDocument/")),
)

OPEN_YOURSELF = "open it yourself"


@dataclass(frozen=True)
class Attachment:
    kind: str    # atc | spec | boq
    url: str
    page: int    # page of the bid PDF that holds the link
    status: str  # read | scanned | not_pdf | too_long | not_fetched
    note: str
    sha256: str | None = None
    pages: list[PageText] = field(default_factory=list)


class AttachmentService:
    def __init__(self, fetcher: SafeFetcher, documents: DocumentStore, extractor: TextExtractor):
        self._fetcher = fetcher
        self._documents = documents
        self._extractor = extractor  # built with MAX_PAGES

    def fetch_for(self, bid_pdf: bytes) -> list[Attachment]:
        links = pdf_links(bid_pdf)
        chosen = [(kind, link) for kind, pattern in ATTACHMENT_KINDS
                  for link in links if pattern.match(link.url)][:MAX_FILES_PER_BID]
        return [self._fetch(kind, link) for kind, link in chosen]

    def _fetch(self, kind: str, link: PdfLink) -> Attachment:
        def result(status: str, note: str, **more) -> Attachment:
            return Attachment(kind, link.url, link.page, status, note, **more)

        if not link.url.lower().endswith(".pdf"):  # a non-PDF would look like a block page
            return result("not_pdf", f"This file is not a PDF; {OPEN_YOURSELF}.")
        try:
            body = self._fetcher.get(link.url, expect=Expect.PDF).body
        except UnexpectedResponse as error:  # missing or too big; breaker and budget stops propagate
            return result("not_fetched", f"GeM did not give this file ({error}); {OPEN_YOURSELF}.")
        sha256 = hashlib.sha256(body).hexdigest()
        self._documents.save(sha256, body)
        try:
            pages = self._extractor.extract(body)
        except InvalidPdf as error:
            status = "too_long" if "pages" in str(error) else "not_pdf"
            return result(status, f"{error}; {OPEN_YOURSELF}.", sha256=sha256)
        if not any(page.text for page in pages):
            return result("scanned", f"This file is a scan with no text; {OPEN_YOURSELF}.", sha256=sha256)
        return result("read", "Read as text.", sha256=sha256, pages=pages)
