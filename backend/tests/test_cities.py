"""Cities he works in: bids that deliver elsewhere are marked, and can be hidden."""

from datetime import datetime, timezone

from gem_assistant.domain.models import Consignee, Evidence, ExtractionMethod, SellerProfile
from gem_assistant.domain.cities import delivers_to_cities

EV = Evidence(page=1, quote="q", method=ExtractionMethod.LABEL_PARSE)


def _row(address, pin="302001"):
    return Consignee(pin=pin, address=address, quantity=1, delivery_days=15, evidence=EV)


def test_match_is_by_whole_word_and_ignores_case():
    rows = [_row("Collectorate, Jaipur, Rajasthan")]
    assert delivers_to_cities(rows, ["jaipur"]) is True
    assert delivers_to_cities(rows, ["Pur"]) is False                 # not inside another word
    assert delivers_to_cities(rows, ["Kota", "Jaipur"]) is True       # any of several cities
    assert delivers_to_cities(rows, ["Kota"]) is False


def test_unknown_when_nothing_to_judge_by():
    assert delivers_to_cities([_row("Jaipur")], []) is None            # no cities set
    assert delivers_to_cities([], ["Jaipur"]) is None                  # no consignee table
    assert delivers_to_cities([_row("*** masked ***", pin=None)], ["Jaipur"]) is None


def test_the_profile_keeps_cities_and_the_rule_asks_for_a_look(container):
    from gem_assistant.eligibility.rules import CityRule
    from gem_assistant.domain.models import BidAnalysis
    profile = container.profiles.save(SellerProfile(cities=["Jaipur", " jaipur ", "Kota"]))
    assert profile.cities == ["Jaipur", "Kota"]
    assert container.profiles.get().cities == ["Jaipur", "Kota"]       # survives saving and loading

    now = datetime(2026, 10, 23, tzinfo=timezone.utc)
    bid = BidAnalysis(bid_number="GEM/2026/B/1", source_name="x", sha256="a" * 64, page_count=1, unread_lines=0,
                      imported_at=now, flags=[], fields=[], consignees=[_row("Collectorate, Jodhpur")])
    (result,) = CityRule().evaluate(bid, profile, now)
    assert result.outcome.value == "NEEDS_REVIEW" and "Jodhpur" in result.reason and "Jaipur" in result.reason
    assert CityRule().evaluate(bid, SellerProfile(), now) == []
    assert CityRule().evaluate(bid.model_copy(update={"consignees": [_row("Jaipur")]}), profile, now) == []
