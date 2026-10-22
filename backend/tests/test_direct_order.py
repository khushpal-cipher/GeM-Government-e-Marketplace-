"""Step 6.3: direct-order check from a product page and its Other Sellers summary (fixtures seen 23 Oct 2026)."""

from decimal import Decimal
from pathlib import Path

import pytest

from gem_assistant.domain.ports import HttpResponse
from gem_assistant.parsing.product_parser import parse_product, parse_sellers_summary
from gem_assistant.safety.response_classifier import Expect, ResponseClassifier, ResponseKind
from gem_assistant.services.direct_order_service import DirectOrderService

FIX = Path(__file__).parent / "fixtures"
PRODUCT = (FIX / "mkp-product_2026-10-23.html").read_text()
SELLERS = (FIX / "mkp-all-sellers_2026-10-23.html").read_text()
LINK = "https://mkp.gem.gov.in/plain-copier-paper-v3-isi-marked-14490/plain-copier-paper-fs-75-gsm/p-5116877-3483486048-cat.html"


def test_parsers_read_the_real_page_shapes():
    assert parse_product(PRODUCT).mrp == Decimal("400.00") and parse_product(PRODUCT).offer_price == Decimal("170.00")
    s = parse_sellers_summary(SELLERS)
    assert (s.offerings, s.price_low, s.price_high) == (623, Decimal("170.0"), Decimal("360.0"))


def _kind(body: str) -> ResponseKind:
    return ResponseClassifier().classify(HttpResponse("https://mkp.gem.gov.in/x", 200, {}, body.encode()),
                                         Expect.PRODUCT_PAGE).kind


def test_pages_with_captcha_in_scripts_are_not_a_block():
    assert "captcha" in PRODUCT.lower() and _kind(PRODUCT) is ResponseKind.OK and _kind(SELLERS) is ResponseKind.OK


def test_challenge_page_is_a_block():
    assert _kind("<html><body>Please solve the captcha</body></html>") is ResponseKind.BLOCK


class _Fetcher:
    def __init__(self):
        self.urls = []

    def get(self, url, expect):
        self.urls.append((url, expect))
        return HttpResponse(url, 200, {}, (SELLERS if url.endswith("all_sellers.html") else PRODUCT).encode())


def _check(price, link=LINK):
    fetcher = _Fetcher()
    return DirectOrderService(fetcher).check(link, Decimal(price)), fetcher


def test_two_public_requests_and_floor_is_mrp_minus_ten_percent():
    result, fetcher = _check("200")
    assert [u.rsplit("/", 1)[1] for u, _ in fetcher.urls] == ["p-5116877-3483486048-cat.html", "all_sellers.html"]
    assert result["lowest_he_can_list"] == "360.00" and result["offerings"] == 623


def test_price_below_floor():
    assert "lowest you can list is ₹360.00" in _check("300")[0]["verdict"]


def test_price_above_floor_but_listings_exist_below_warns_about_location():
    # The floor (360) is above the cheapest listing (170), so any legal price meets a lower listing.
    assert "does not show where" in _check("365")[0]["verdict"]


@pytest.mark.parametrize("link", ["http://mkp.gem.gov.in/a/b/p-1-2-cat.html", "https://evil.example/a/b/p-1-2-cat.html",
                                  "https://mkp.gem.gov.in/search?q=x"])
def test_only_product_links_are_fetched(link):
    fetcher = _Fetcher()
    with pytest.raises(ValueError):
        DirectOrderService(fetcher).check(link, Decimal("400"))
    assert fetcher.urls == []
