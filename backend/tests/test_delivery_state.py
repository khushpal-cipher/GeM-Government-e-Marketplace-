"""Step 3.1: delivery state, from the consignee PINs against the states he delivers to."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from gem_assistant.domain.india_states import normalise_states, states_for_pin
from gem_assistant.domain.models import (
    BidAnalysis, ClauseFlag, Consignee, Evidence, ExtractionMethod, SellerProfile,
)
from gem_assistant.domain.profile_warnings import profile_warnings
from gem_assistant.eligibility.rules import DEFAULT_RULES, DeliveryStateRule, RestrictiveClauseRule
from gem_assistant.parsing.clause_scanner import PatternClauseScanner
from gem_assistant.domain.models import PageText

AT = datetime(2026, 10, 22, tzinfo=timezone.utc)
EV = Evidence(page=2, quote="row", method=ExtractionMethod.LABEL_PARSE)


def _bid(pins, flags=()) -> BidAnalysis:
    rows = [Consignee(pin=p, address=a, quantity=q, delivery_days=15, evidence=EV) for p, a, q in pins]
    return BidAnalysis(bid_number="GEM/2026/B/1", source_name="x.pdf", sha256="a" * 64, page_count=1,
                       unread_lines=0, imported_at=AT, fields=[], flags=list(flags), consignees=rows)


def _run(bid, states):
    return DeliveryStateRule().evaluate(bid, SellerProfile(states=states), AT)


# Real PINs from the corpus/fixtures: Nashik, Varanasi, Udaipur, Hubli.
@pytest.mark.parametrize("pin, expected", [
    ("422001", {"Maharashtra"}), ("221001", {"Uttar Pradesh"}), ("313001", {"Rajasthan"}),
    ("580020", {"Karnataka"}), ("248001", {"Uttar Pradesh", "Uttarakhand"}),
    ("110001", {"Delhi"}), ("900001", set()), (None, set()), ("12", set()),
])
def test_pin_to_states(pin, expected):
    assert states_for_pin(pin) == expected


def test_profile_aliases():
    assert normalise_states(["UP", "m.p.", "Orissa", "J&K", "NCT of Delhi", "Pondicherry"])[0] == {
        "Uttar Pradesh", "Madhya Pradesh", "Odisha", "Jammu and Kashmir", "Delhi", "Puducherry"}
    assert normalise_states(["Atlantis"]) == (set(), ["Atlantis"])


def test_silent_when_inside_his_states_or_nothing_to_compare():
    bid = _bid([("221001", "Varanasi", 2), ("221002", "Varanasi", 1)])
    assert _run(bid, ["UP"]) == []
    assert _run(bid, []) == []
    assert _run(_bid([]), ["UP"]) == []


def test_other_state_is_a_review_never_a_block():
    (r,) = _run(_bid([("580020", "Hubli", 3), ("580021", "Hubli", 1)]), ["Maharashtra"])
    assert r.outcome.value == "NEEDS_REVIEW"
    assert "Karnataka" in r.reason and "2 rows" in r.reason and "4 units" in r.reason
    assert r.evidence == EV


def test_partly_overlapping_state_set():
    (r,) = _run(_bid([("248001", "Dehradun", 1)]), ["Uttar Pradesh"])
    assert r.outcome.value == "NEEDS_REVIEW" and "248001" in r.reason and "Uttarakhand" in r.reason


def test_masked_or_unknown_pins_make_one_review():
    bid = _bid([(None, "***AMRITSAR RURAL", 1), (None, "***JALANDHAR", 1), ("900001", "APO", 1)])
    (r,) = _run(bid, ["Punjab"])
    assert "masked" in r.reason and "3 rows" in r.reason and "AMRITSAR RURAL" in r.reason


def test_a_profile_state_no_alias_knows_is_ignored_and_warned():
    assert _run(_bid([("580020", "Hubli", 1)]), ["Atlantis"]) == []
    assert any("Atlantis" in w for w in profile_warnings(SellerProfile(states=["Atlantis"]), AT.date()))


@pytest.mark.parametrize("text", [
    "AVAILABILITY OF OFFICE OF SERVICE PROVIDER: An office of the Service Provider must be located in the state of Consignee.",
    "Office registered in the city of Visakhapatnam is mandatory.",
])
def test_local_presence_clause_is_found_and_reviewed_once(text):
    page = PageText(number=3, text=f"/Buyer Added Bid Specific Terms and Conditions\n{text}\n/Disclaimer\n")
    flags = PatternClauseScanner().scan([page])
    assert [f.category for f in flags] == ["local_presence"]
    bid = _bid([], flags)
    (r,) = _run(bid, [])  # even with no states in the profile
    assert "local office" in r.reason and text.split(": ")[-1][:20] in r.reason
    assert RestrictiveClauseRule().evaluate(bid, None, AT) == []
    assert DeliveryStateRule in {type(x) for x in DEFAULT_RULES}
