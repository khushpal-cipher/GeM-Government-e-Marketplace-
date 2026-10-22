"""Step 2.3: the files a bid PDF links to (buyer ATC file, specification PDF, BOQ detail)."""

from __future__ import annotations

import hashlib
import io

import pytest
from pypdf import PdfWriter

from gem_assistant.safety.errors import SafetyError

from .conftest import FIXTURES, SAMPLE_PDF

SPEC_PDF = (FIXTURES / "attachment-spec_2026-10-22.pdf").read_bytes()
SPEC_URL = "https://mkp.gem.gov.in/catalog_data/x/CatalogAttrs/SpecificationDocument/2025/10/24/spec.pdf"
ATC_URL = "https://fulfilment.gem.gov.in/contract/slafds?fileDownloadPath=SLA_UPLOAD_PATH/2025/Oct/X/ATC_1.pdf"
BOQ_URL = "https://mkp.gem.gov.in/uploaded_documents/x/OrderItem/BoqDocument/2025-10-24/tech.pdf"


def _blank_pdf(pages: int = 1) -> bytes:
    writer, out = PdfWriter(), io.BytesIO()
    for _ in range(pages):
        writer.add_blank_page(595, 842)
    writer.write(out)
    return out.getvalue()


def test_real_bid_pdf_links_are_fetched_atc_first_then_spec(container, transport):
    transport.queue(body=_blank_pdf())  # the scanned ATC file
    transport.queue(body=SPEC_PDF)
    found = container.attachments.fetch_for(SAMPLE_PDF.read_bytes())
    assert [(a.kind, a.status) for a in found] == [("atc", "scanned"), ("spec", "read")]
    assert [url for url, _ in transport.calls][0].startswith("https://fulfilment.gem.gov.in/contract/slafds?")
    spec = found[1]
    assert "Display size" in spec.pages[0].text and spec.sha256 == hashlib.sha256(SPEC_PDF).hexdigest()
    assert "scanned" in found[0].note.lower() or "open it yourself" in found[0].note.lower()


def test_files_are_kept_by_hash(container, transport, settings):
    transport.queue(body=_blank_pdf())
    transport.queue(body=SPEC_PDF)
    container.attachments.fetch_for(SAMPLE_PDF.read_bytes())
    assert (settings.data_dir / "documents" / f"{hashlib.sha256(SPEC_PDF).hexdigest()}.pdf").exists()


def test_at_most_three_files_per_bid(container, transport, monkeypatch):
    from gem_assistant.infrastructure.pypdf_extractor import PdfLink
    from gem_assistant.services import attachment_service

    links = [PdfLink(1, ATC_URL), PdfLink(1, SPEC_URL), PdfLink(2, BOQ_URL),
             PdfLink(2, BOQ_URL.replace("tech", "more"))]
    monkeypatch.setattr(attachment_service, "pdf_links", lambda _pdf: links)
    for _ in range(3):
        transport.queue(body=SPEC_PDF)
    found = container.attachments.fetch_for(b"ignored")
    assert [a.kind for a in found] == ["atc", "spec", "boq"] and len(transport.calls) == 3


def test_a_non_pdf_file_is_not_requested_at_all(container, transport, monkeypatch):
    from gem_assistant.infrastructure.pypdf_extractor import PdfLink
    from gem_assistant.services import attachment_service

    docx = ATC_URL.replace("ATC_1.pdf", "ATC_1.docx")
    monkeypatch.setattr(attachment_service, "pdf_links", lambda _pdf: [PdfLink(1, docx)])
    found = container.attachments.fetch_for(b"ignored")
    assert [(a.status, a.sha256) for a in found] == [("not_pdf", None)] and transport.calls == []
    assert "open it yourself" in found[0].note.lower()


def test_a_missing_file_is_reported_and_the_rest_still_load(container, transport):
    transport.queue(status=404, body=b"")
    transport.queue(body=SPEC_PDF)
    found = container.attachments.fetch_for(SAMPLE_PDF.read_bytes())
    assert [a.status for a in found] == ["not_fetched", "read"]


def test_a_pdf_over_the_page_cap_is_not_read(container, transport, monkeypatch):
    from gem_assistant.infrastructure.pypdf_extractor import PdfLink
    from gem_assistant.services import attachment_service

    monkeypatch.setattr(attachment_service, "pdf_links", lambda _pdf: [PdfLink(1, SPEC_URL)])
    transport.queue(body=_blank_pdf(101))
    assert container.attachments.fetch_for(b"ignored")[0].status == "too_long"


def test_a_safety_stop_is_not_swallowed(container, transport):
    transport.queue(status=403, body=b"denied")
    transport.queue(body=SPEC_PDF)
    with pytest.raises(SafetyError):
        container.attachments.fetch_for(SAMPLE_PDF.read_bytes())
