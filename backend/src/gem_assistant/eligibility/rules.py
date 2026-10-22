"""Eligibility rules. Each rule checks one thing (Single Responsibility).

Rules are plain deterministic code. They never call an LLM. To add a check,
write a new class with `name` and `evaluate()` and add it to DEFAULT_RULES.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from typing import Callable

from ..domain.models import (
    BidAnalysis, Consignee, Evidence, SpecRow, CorrigendumStatus, FieldStatus, RuleResult, SellerProfile, Verdict, item_match,
)
from ..domain.wording import day, deadline
from ..domain.cities import delivers_to_cities
from ..domain.india_states import normalise_states, states_for_pin
from ..parsing.clause_patterns import DEFAULT_CLAUSE_PATTERNS

_BLOCKING_CATEGORIES = {p.category for p in DEFAULT_CLAUSE_PATTERNS if p.blocking_hint}


def inr(rupees: int) -> str:
    """25500000 -> '₹2,55,00,000' (Indian digit grouping)."""
    digits = str(rupees)
    head, tail = digits[:-3], digits[-3:]
    groups: list[str] = []
    while len(head) > 2:
        groups.insert(0, head[-2:])
        head = head[:-2]
    return "₹" + ",".join(part for part in (head, *groups, tail) if part)


class ProfileRequiredRule:
    name = "profile_required"

    def evaluate(self, bid: BidAnalysis, profile: SellerProfile | None, now: datetime) -> list[RuleResult]:
        if profile is None:
            return [RuleResult(rule=self.name, outcome=Verdict.NEEDS_REVIEW,
                               reason="No seller profile saved yet, so eligibility can't be checked.")]
        return []


class DeadlineRule:
    """The bid document holds the original deadline, and a corrigendum can extend it — seen
    live on 11-Oct-2026, when three bids whose PDFs said they closed on 5-7 Oct were open
    until the 12th. So a passed deadline only blocks once GeM has confirmed there is no
    corrigendum, and confirmed it after that deadline (an earlier answer cannot know about a
    later extension). Otherwise the bid needs a look: skipping a live bid costs a bid."""

    name = "deadline"

    def evaluate(self, bid: BidAnalysis, profile: SellerProfile | None, now: datetime) -> list[RuleResult]:
        if bid.found_value("bid_end") is None:
            return []  # missing critical fields are handled by CriticalFieldsRule
        field = bid.field("bid_end")
        deadline = bid.deadline()  # GeM's listing, when later, carries any extension
        if deadline > now:
            return []
        checked_at = bid.corrigendum.checked_at
        if bid.corrigendum.status is CorrigendumStatus.NONE and checked_at is not None and checked_at >= deadline:
            return [RuleResult(rule=self.name, outcome=Verdict.BLOCKED,
                               reason="Bid has already closed.", evidence=field.evidence)]
        return [RuleResult(rule=self.name, outcome=Verdict.NEEDS_REVIEW,
                           reason="The deadline in the bid document has passed, but it may have been extended "
                                  "by a corrigendum. Check the current deadline on GeM.",
                           evidence=field.evidence)]


class CriticalFieldsRule:
    name = "critical_fields"

    def evaluate(self, bid: BidAnalysis, profile: SellerProfile | None, now: datetime) -> list[RuleResult]:
        results = []
        for f in bid.fields:
            if not f.critical or f.status is FieldStatus.FOUND:
                continue
            reason = {
                FieldStatus.NOT_FOUND: f"Couldn't find “{f.label}” in the document. Check it by hand.",
                FieldStatus.UNCLEAR: f"“{f.label}” was found but couldn't be read reliably.",
                FieldStatus.CONFLICTING: f"“{f.label}” conflicts with a buyer clause. {f.note or ''}",
            }[f.status]
            results.append(RuleResult(rule=self.name, outcome=Verdict.NEEDS_REVIEW,
                                      reason=reason.strip(), evidence=f.evidence))
        return results


class ConflictingFieldsRule:
    """Non-critical fields can still conflict; surface those too."""

    name = "conflicts"

    def evaluate(self, bid: BidAnalysis, profile: SellerProfile | None, now: datetime) -> list[RuleResult]:
        return [
            RuleResult(rule=self.name, outcome=Verdict.NEEDS_REVIEW,
                       reason=f"“{f.label}” conflicts with a buyer clause. {f.note or ''}".strip(),
                       evidence=f.evidence)
            for f in bid.fields
            if not f.critical and f.status is FieldStatus.CONFLICTING
        ]


class RestrictiveClauseRule:
    name = "restrictive_clauses"

    def evaluate(self, bid: BidAnalysis, profile: SellerProfile | None, now: datetime) -> list[RuleResult]:
        return [
            RuleResult(rule=self.name, outcome=Verdict.NEEDS_REVIEW,
                       reason=f"{flag.label}: read this clause and confirm you qualify.",
                       evidence=flag.evidence)
            for flag in bid.flags
            if flag.category in _BLOCKING_CATEGORIES and flag.category != "oem_authorisation"
        ]


class UnreadAttachmentRule:
    name = "unread_attachment"

    def evaluate(self, bid: BidAnalysis, profile: SellerProfile | None, now: datetime) -> list[RuleResult]:
        return [
            RuleResult(rule=self.name, outcome=Verdict.NEEDS_REVIEW,
                       reason="The buyer attached a separate terms document. Open it on GeM and read it; "
                              "this tool has not checked it.",
                       evidence=flag.evidence)
            for flag in bid.flags
            if flag.category == "unread_attachment"
        ]


class CorrigendumRule:
    """A corrigendum can move the deadline or change the specification, so every state
    except "GeM says there is none" is something the person must look at.

    NOT_CHECKED is deliberately not silent: a bid we could not check is a bid whose
    facts may already be out of date.
    """

    name = "corrigendum"

    _REASONS = {
        CorrigendumStatus.PRESENT:
            "This bid has a corrigendum. It can change the deadline, quantity, "
            "specification or terms — read it before relying on anything below.",
        CorrigendumStatus.NOT_CHECKED:
            "Not checked for a corrigendum. Open the bid on GeM and use "
            "“View Corrigendum/Representation” before you bid.",
        CorrigendumStatus.FAILED:
            "The corrigendum check did not complete, so this bid may have been amended "
            "without us seeing it. Check it on GeM.",
    }

    def evaluate(self, bid: BidAnalysis, profile: SellerProfile | None, now: datetime) -> list[RuleResult]:
        reason = self._REASONS.get(bid.corrigendum.status)
        if reason is None:  # NONE: GeM told us there is no corrigendum
            return []
        note = f" {bid.corrigendum.note}" if bid.corrigendum.note else ""
        return [RuleResult(rule=self.name, outcome=Verdict.NEEDS_REVIEW, reason=f"{reason}{note}")]


class EmdRule:
    """EMD is a step to plan, not a bar, so this only ever asks for a look. An amount alone also means it is asked."""

    name = "emd"
    _MIN_VALUE = 500_000  # GeM's terms: no EMD on a bid estimated below ₹5 lakh

    def evaluate(self, bid: BidAnalysis, profile: SellerProfile | None, now: datetime) -> list[RuleResult]:
        amount = bid.found_value("emd_amount")
        if bid.found_value("emd_required") != "Yes" and not (amount and int(amount) > 0):
            return []
        field = bid.field("emd_required") if bid.found_value("emd_required") == "Yes" else bid.field("emd_amount")
        what = f"EMD {inr(int(amount))}" if amount else "EMD"
        due = bid.deadline()
        when = deadline(due, now) if due else "before the bid closes"
        value = bid.found_value("estimated_bid_value")
        if value and int(value) < self._MIN_VALUE:
            reason = (f"This bid asks an {what}, but its estimated value is {inr(int(value))} (below ₹5 lakh); "
                      f"GeM's terms say no EMD below ₹5 lakh. You may ask the buyer through a representation {when}.")
            return [RuleResult(rule=self.name, outcome=Verdict.NEEDS_REVIEW, reason=reason, evidence=field.evidence)]
        makes = profile is not None and item_match(bid.found_value("item_category"), profile.own_made_products,
                                                   profile.ignore_words)[0] > 0
        if profile and (profile.is_startup or (profile.is_mse and makes)):
            who = "DPIIT startup" if profile.is_startup else "MSE making this item"
            limit = next((f.evidence for f in bid.flags if f.category == "emd_state_limit"), None)
            reason = (f"{what}: you may be exempt ({who}). Claim it with your Udyam / DPIIT certificate when you bid."
                      + (f" The buyer limits it: “{limit.quote}”" if limit else ""))
        elif profile and profile.is_mse and not profile.own_made_products:
            reason = (f"{what}. MSEs are exempt only for items they make; add the items you make to your "
                      "profile to check.")
        elif profile and profile.is_mse:
            reason = (f"{what}: the MSE exemption covers only items you make, so pay it before the bid closes "
                      f"({when}).")
        else:
            reason = f"Pay an {what.replace('EMD ', 'EMD of ') if amount else 'EMD'} before the bid closes ({when})."
        return [RuleResult(rule=self.name, outcome=Verdict.NEEDS_REVIEW, reason=reason, evidence=field.evidence)]


@dataclass(frozen=True)
class _Requirement:
    field: str              # the bid's stated minimum
    profile_attr: str       # the seller's figure
    mse_relaxation: str
    startup_relaxation: str
    what: str
    show: Callable[[int], str]


class TurnoverExperienceRule:
    """Compares the bid's stated minimum turnover and experience with the seller profile.

    Blocks only on a clear shortfall that no relaxation covers. Whatever it cannot decide — a
    partial relaxation, a relaxation it could not read, a profile without the figure — is a
    review, never a block: skipping a bid the seller could win costs a bid."""

    name = "turnover_experience"

    _REQUIREMENTS = (
        _Requirement("min_avg_turnover", "annual_turnover_rupees", "mse_turnover_relaxation",
                     "startup_turnover_relaxation", "average annual turnover (last 3 years)", inr),
        _Requirement("min_experience_years", "years_experience", "mse_experience_relaxation",
                     "startup_experience_relaxation", "years of experience", lambda n: f"{n} years"),
    )

    def evaluate(self, bid: BidAnalysis, profile: SellerProfile | None, now: datetime) -> list[RuleResult]:
        if profile is None:
            return []
        return [r for req in self._REQUIREMENTS if (r := self._check(req, bid, profile)) is not None]

    def _check(self, req: _Requirement, bid: BidAnalysis, profile: SellerProfile) -> RuleResult | None:
        field = bid.field(req.field)
        if field is None or field.status is FieldStatus.NOT_FOUND:
            return None
        if field.status is not FieldStatus.FOUND:
            return self._result(Verdict.NEEDS_REVIEW, f"The bid states a minimum {req.what} that couldn't be "
                                                      "read reliably. Check it in the document.", field)
        required = int(field.value)
        applicable = [name for name, applies in ((req.mse_relaxation, profile.is_mse),
                                                 (req.startup_relaxation, profile.is_startup)) if applies]
        relaxations = {bid.found_value(name) for name in applicable}  # None = not found or unreadable
        if "Yes" in relaxations:
            return None
        have = getattr(profile, req.profile_attr)
        if have is None:
            return self._result(Verdict.NEEDS_REVIEW, f"The bid requires a minimum {req.what} of "
                                f"{req.show(required)}. Add yours to the seller profile to check it.", field)
        if have >= required:
            return None
        shortfall = f"The bid requires a minimum {req.what} of {req.show(required)}; your profile says {req.show(have)}."
        if relaxations - {"No"}:  # partial, or a relaxation for your category we couldn't read
            return self._result(Verdict.NEEDS_REVIEW, f"{shortfall} A relaxation may apply to you (partial, or "
                                                      "not readable here). Check the bid's terms.", field)
        return self._result(Verdict.BLOCKED, shortfall, field)

    def _result(self, outcome: Verdict, reason: str, field) -> RuleResult:
        return RuleResult(rule=self.name, outcome=outcome, reason=reason, evidence=field.evidence)


class DeliveryStateRule:
    """Consignee states (from the PIN) against the states he delivers to. His states are a preference,
    so this only ever asks for a look. Also owns the `local_presence` clause (docs/checks-design.md 3.1)."""

    name = "delivery_state"

    def evaluate(self, bid: BidAnalysis, profile: SellerProfile | None, now: datetime) -> list[RuleResult]:
        results = [RuleResult(rule=self.name, outcome=Verdict.NEEDS_REVIEW, evidence=f.evidence,
                              reason=f"The buyer asks for a local office: “{f.evidence.quote}”. "
                                     "Check you have one there.")
                   for f in bid.flags if f.category == "local_presence"]
        mine = normalise_states(profile.states)[0] if profile else set()
        if not mine:
            return results
        groups: dict[frozenset[str], list[Consignee]] = {}
        masked: list[Consignee] = []
        for row in bid.consignees:
            found = frozenset(states_for_pin(row.pin))
            if not found:
                masked.append(row)
            elif not found <= mine:
                groups.setdefault(found, []).append(row)
        for found, rows in groups.items():
            first, units = rows[0], sum(r.quantity for r in rows)
            names = " or ".join(sorted(found))
            if found & mine:
                reason = f"Delivery to PIN {first.pin} ({names}): check it is a state you deliver to."
            else:
                reason = (f"Delivery to {names} ({len(rows)} rows, {units} units): not one of the states you "
                          "deliver to. Price the freight to the consignee, or skip.")
            results.append(RuleResult(rule=self.name, outcome=Verdict.NEEDS_REVIEW, reason=reason,
                                      evidence=first.evidence))
        if masked:
            places = ", ".join(dict.fromkeys(r.address.strip("* ") for r in masked))[:120]
            results.append(RuleResult(rule=self.name, outcome=Verdict.NEEDS_REVIEW, evidence=masked[0].evidence,
                                      reason=f"Delivery place masked by the buyer: {places} ({len(masked)} rows). "
                                             "Check its state."))
        return results


class CityRule:
    """He works in some cities; a bid delivering to none of them is worth a look, never a block."""

    name = "delivery_city"

    def evaluate(self, bid: BidAnalysis, profile: SellerProfile | None, now: datetime) -> list[RuleResult]:
        if not profile or delivers_to_cities(bid.consignees, profile.cities) is not False:
            return []
        places = "; ".join(dict.fromkeys(" ".join(c.address.split())[:60] for c in bid.consignees))[:150]
        return [RuleResult(rule=self.name, outcome=Verdict.NEEDS_REVIEW, evidence=bid.consignees[0].evidence,
                           reason=f"Delivery to {places}: none of the cities you work in ({', '.join(profile.cities)}).")]


_STANDARD = re.compile(r"\b(ISO(?:\s*/\s*IEC)?\s*(\d{3,5})(?::\d{4})?|I\s?S\s*:?\s*(\d{2,5})|(BIS)|(NABL))\b",
                       re.IGNORECASE)


def standards_in(text: str) -> list[str]:
    """Named standards in `text`, by number, in order: 'ISO/IEC 27001:2013' -> 'ISO 27001'. A bare 'ISO' is none."""
    found = ((f"ISO {m[2]}" if m[2] else f"IS {m[3]}" if m[3] else (m[4] or m[5]).upper()) for m in _STANDARD.finditer(text))
    return list(dict.fromkeys(found))


class CertificateRule:
    """Named standards the bid asks for, against his certificates, matched by number (a bare "ISO" in the
    profile covers none). The profile list is free text he may not have finished, so never a block."""

    name = "certificates"

    def evaluate(self, bid: BidAnalysis, profile: SellerProfile | None, now: datetime) -> list[RuleResult]:
        if profile is None:
            return []
        asked: dict[str, Evidence] = {}
        for flag in bid.flags:
            if flag.category == "certification":
                for s in standards_in(flag.evidence.quote):
                    asked.setdefault(s, flag.evidence)
        item = bid.field("item_category")
        if item and item.value and item_match(item.value, profile.oem_products, profile.ignore_words)[0]:
            for s in standards_in(item.value):  # a product standard is held by its maker
                if s.startswith("IS "):
                    asked.setdefault(s, item.evidence)
        have = {s for c in profile.certifications for s in standards_in(c)}
        missing = {s: ev for s, ev in asked.items() if s not in have}
        if not missing:
            return []
        shown = lambda s: f"{s} (page {missing[s].page}: “{missing[s].quote}”)"
        if not profile.certifications:
            quotes = dict.fromkeys(f"page {e.page}: “{e.quote}”" for e in missing.values())
            return [RuleResult(rule=self.name, outcome=Verdict.NEEDS_REVIEW, evidence=next(iter(missing.values())),
                               reason=f"The bid asks for {', '.join(missing)} ({'; '.join(quotes)}). "
                                      "Add your certificates to the profile to check them.")]
        listed = ", ".join(profile.certifications)
        return [RuleResult(rule=self.name, outcome=Verdict.NEEDS_REVIEW, evidence=ev,
                           reason=f"The bid asks for {shown(s)}; your profile lists {listed}. "
                                  "Attach it if you have it, or skip.")
                for s, ev in missing.items()]


_QUADRANT = re.compile(r"\(Q([12])\)")


class OemRule:
    """A reseller (not the maker of this bid's item) needs the maker's authorisation, and sometimes the
    maker's turnover. He is the maker when `is_oem` and his `oem_products` are empty or name the item.
    `is_oem` cannot tell "no" from "not answered", so this never blocks."""

    name = "oem"

    def evaluate(self, bid: BidAnalysis, profile: SellerProfile | None, now: datetime) -> list[RuleResult]:
        if profile is None:
            return []
        item = bid.field("item_category")
        item_text = bid.found_value("item_category")
        if profile.is_oem and (not profile.oem_products or item_match(
                item_text, profile.oem_products, profile.ignore_words)[0]):
            return []
        docs = bid.field("documents_required")
        entries = (bid.found_value("documents_required") or "").lower()
        auth = next((f.evidence for f in bid.flags if f.category == "oem_authorisation"), None)
        if auth is None and "oem authori" in entries:
            auth = docs.evidence
        turnover = docs.evidence if "oem annual turnover" in entries else None
        tags = set(_QUADRANT.findall(item_text or ""))
        if auth is None and "2" in tags:
            auth = item.evidence
        due = bid.deadline()
        when = f" before the bid closes ({deadline(due, now)})" if due else ""
        if auth is not None or turnover is not None:
            wants = ["an OEM authorisation certificate"] * (auth is not None) + \
                    ["the maker's turnover certificate (CA certified)"] * (turnover is not None)
            ev = auth or turnover
            return [RuleResult(rule=self.name, outcome=Verdict.NEEDS_REVIEW, evidence=ev,
                               reason=f"The bid asks for {' and '.join(wants)} (page {ev.page}: “{ev.quote}”). "
                                      f"As a reseller, get them from the maker of the product you offer{when}.")]
        if "1" in tags:
            return [RuleResult(rule=self.name, outcome=Verdict.NEEDS_REVIEW, evidence=item.evidence,
                               reason="GeM lists this item in Q1: only its maker (OEM) can offer it. Your profile "
                                      "says you are not the OEM of it. (GeM rule not confirmed; check on GeM)")]
        return []


class PacRule:
    """A PAC (Proprietary Article Certificate) bid names one make. His profile has no list of makes he is
    authorised for, so it is a look, never a block."""

    name = "pac"

    def evaluate(self, bid: BidAnalysis, profile: SellerProfile | None, now: datetime) -> list[RuleResult]:
        evidence = [f.evidence for f in bid.flags if f.category == "pac"]
        if bid.found_value("pac_mode"):
            evidence.append(bid.field("pac_mode").evidence)
        return [RuleResult(rule=self.name, outcome=Verdict.NEEDS_REVIEW, evidence=ev,
                           reason=f"This is a PAC bid: only the named make can be offered (page {ev.page}: “{ev.quote}”). "
                                  "Bid only if you sell that make, with the maker's authorisation.")
                for ev in evidence]


# GeM's list of buyer terms that make a bid "null & void": item number and its words in the list.
_FORBIDDEN = {
    "forbidden_brand": (2, "Mandating procurement of / from specific Brand / Make / Model / Manufacturer / Dealer"),
    "forbidden_physical": (4, "Mandating submission of documents in physical form as a pre-requisite to qualify bidders"),
    "forbidden_sample": (7, "Seeking sample with bid or approval of samples during bid evaluation process"),
    "forbidden_experience": (8, "Seeking experience from specific organization / department / institute only or from "
                                "foreign / export experience"),
    "forbidden_external": (10, "Reference of conditions published on any external site or reference to external documents"),
    "forbidden_fee": (11, "Asking for any Tender fee / Bid Participation fee"),
}
_IST = timezone(timedelta(hours=5, minutes=30))


def representation_deadline(dated: date, end: datetime) -> datetime | None:
    """Last moment to ask the buyer (GeM SFAQ): open 10+ days -> start + 4 days, 6-9 -> +2, 3-5 -> +1, to the end
    of that day. None when the bid is open under 3 days."""
    open_days = (end.astimezone(_IST).date() - dated).days
    extra = 4 if open_days >= 10 else 2 if open_days >= 6 else 1 if open_days >= 3 else None
    return None if extra is None else datetime.combine(dated + timedelta(days=extra), time(23, 59, 59), _IST)


class ForbiddenTermRule:
    """A buyer term GeM's list says may not be added is the buyer's mistake, not his: a look, never a block."""

    name = "forbidden_terms"

    def evaluate(self, bid: BidAnalysis, profile: SellerProfile | None, now: datetime) -> list[RuleResult]:
        flags = [f for f in bid.flags if f.category in _FORBIDDEN]
        if not flags:
            return []
        dated, end = bid.found_value("bid_dated"), bid.deadline()
        last = representation_deadline(date.fromisoformat(dated), end) if dated and end else None
        if last is None and dated and end:
            tail = "The time to ask the buyer has passed (the bid was open under 3 days); bid on the terms as written, or skip."
        elif last is None:
            tail = "The bid's start date is unknown; check on GeM how long you have to ask the buyer."
        elif last < now:
            tail = f"The time to ask the buyer has passed ({day(last.date())}); bid on the terms as written, or skip."
        else:
            tail = f"You can ask the buyer to remove it with the Representation window in the bid details, {deadline(last, now)}."
        if last is None and not dated:
            tail = tail.replace("The bid's start date is unknown", "The bid's start date is unknown (date unknown; check on GeM)")
        results = []
        for flag in flags:
            number, words = _FORBIDDEN[flag.category]
            results.append(RuleResult(
                rule=self.name, outcome=Verdict.NEEDS_REVIEW, evidence=flag.evidence,
                reason=f"This term may be one GeM does not let buyers add (GeM's list in this bid, item {number}: "
                       f"“{words}”): “{flag.evidence.quote}”. {tail} Only one representation per bid."))
        return results


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9.]+", " ", text.lower()).strip()


def _number(text: str) -> float | None:
    m = re.fullmatch(r"(\d+(?:\.\d+)?)(?:\s*[a-z%/²³]+)?", text.strip().lower().replace(",", ""))
    return float(m[1]) if m else None


def spec_allows(allowed: str, mine: str) -> bool | None:
    """Is his value one the buyer allows? True / False, or None when the two cannot be compared (a text value
    against numbers). The buyer's list is comma-separated; "a to b" is a band; "Or higher" ends the last."""
    higher = bool(re.search(r"\bor higher\s*$", allowed, re.IGNORECASE))
    options = [o.strip() for o in re.sub(r"\s*\bor higher\s*$", "", allowed, flags=re.IGNORECASE).split(",")]
    options = [o for o in options if o]
    want, value = _norm(mine), _number(mine)
    numeric = False
    for i, option in enumerate(options):
        if _norm(option) == want or set(_norm(want).split()) <= set(_norm(option).split()):
            return True
        band = re.fullmatch(r"(\d+(?:\.\d+)?)\s+to\s+(\d+(?:\.\d+)?)", option.strip().lower())
        low = _number(option)
        if band:
            numeric = True
            if value is not None and float(band[1]) <= value <= float(band[2]):
                return True
        elif low is not None:
            numeric = True
            if value is not None and (value == low or (higher and i == len(options) - 1 and value >= low)):
                return True
    return None if numeric and value is None else False


class SpecMatchRule:
    """The buyer's allowed values against the key specs of the products he typed in (step 3.9). His five products
    are not his whole catalogue, so a mismatch is a look, never a block."""

    name = "spec_match"

    def evaluate(self, bid: BidAnalysis, profile: SellerProfile | None, now: datetime) -> list[RuleResult]:
        if profile is None or not bid.specifications:
            return []
        tables: list[list[SpecRow]] = [[]]
        seen: set[str] = set()
        for row in bid.specifications:  # a spec name repeating starts the next item's table
            key = _norm(row.name)
            if key in seen:
                tables.append([])
                seen = set()
            seen.add(key)
            tables[-1].append(row)
        results = []
        for product in profile.products:
            if not item_match(bid.found_value("item_category"), [product.name], profile.ignore_words)[0]:
                continue
            mine = {_norm(k): (k, v) for k, v in product.specs.items()}
            per_table = [[(row, mine[_norm(row.name)]) for row in table
                          if _norm(row.name) in mine and spec_allows(row.value, mine[_norm(row.name)][1]) is False]
                         for table in tables]
            if all(per_table):
                row, (spec, value) = min(per_table, key=len)[0]
                results.append(RuleResult(
                    rule=self.name, outcome=Verdict.NEEDS_REVIEW, evidence=row.evidence,
                    reason=f"Your product “{product.name}” has {spec} = {value}; this bid allows only {row.value} "
                           f"(page {row.page}: “{row.evidence.quote}”). Offer a product that matches exactly."))
        return results


class CategoryMatchRule:
    name = "category_match"

    def evaluate(self, bid: BidAnalysis, profile: SellerProfile | None, now: datetime) -> list[RuleResult]:
        if profile is None or not profile.categories:
            return []
        items = bid.field("item_category")
        hits, total = item_match(bid.found_value("item_category"), profile.categories, profile.ignore_words)
        if hits == 0 and not item_match(bid.found_value("relevant_categories"), profile.categories,
                                        profile.ignore_words)[0]:
            return [RuleResult(rule=self.name, outcome=Verdict.NEEDS_REVIEW,
                               reason="None of the items in this bid is one of your products.",
                               evidence=items.evidence if items else None)]
        method = bid.field("evaluation_method")
        if 0 < hits < total and "total value" in (bid.found_value("evaluation_method") or "").lower():
            # A reseller might source the rest, so this is a look, not a block.
            mine = "1 is one of your products" if hits == 1 else f"{hits} are your products"
            return [RuleResult(rule=self.name, outcome=Verdict.NEEDS_REVIEW,
                               reason=f"This bid is judged on total value, so you must quote for all {total} "
                                      f"items; {mine}.",
                               evidence=method.evidence if method else None)]
        return []


DEFAULT_RULES = (
    ProfileRequiredRule(),
    DeadlineRule(),
    CriticalFieldsRule(),
    ConflictingFieldsRule(),
    UnreadAttachmentRule(),
    CorrigendumRule(),
    RestrictiveClauseRule(),
    EmdRule(),
    TurnoverExperienceRule(),
    DeliveryStateRule(),
    CityRule(),
    CertificateRule(),
    OemRule(),
    PacRule(),
    ForbiddenTermRule(),
    SpecMatchRule(),
    CategoryMatchRule(),
)
