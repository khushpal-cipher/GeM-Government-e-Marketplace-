# Checks design: when the app says "blocked" (step 3.0, 22 Oct 2026)

Fixes, before any code, what each Phase 3 check (3.1-3.9) reads, when it says BLOCKED, when NEEDS_REVIEW,
when it stays silent, and its words. Each check is one class in `eligibility/rules.py`, added to
`DEFAULT_RULES`, with table-driven tests built from the cases below. Facts come from the 30 corpus bids
(`<data folder>/corpus/20261022-0920/`) and the repo fixtures, read 22 Oct 2026.

## In simple words

A wrong "blocked" hides a bid he could win; a wrong "review" costs him one minute of reading. So in Phase 3
**no check ever says BLOCKED**. Each check either says nothing (no problem found) or says "review" with the
buyer's exact words, what his profile says, and what to do. The only blocks stay the two that exist today:
the bid has closed (GeM confirmed no extension), and his turnover or experience is clearly below the bid's
minimum with no relaxation for him. This is decision **D9** (default; see `build-plan.md`).

## Re-verified first (steps 1.1 and 2.1)

- **1.1 profile**: `is_mse`, `is_startup`, `is_oem`, `oem_products`, `own_made_products`, `states`,
  `certifications`, `categories`, `gem_registered_on`, `itr_filed_on_gem`, `pfms_bank_verified` all exist.
  `is_oem` is a plain yes/no that starts as "no", so "he said no" and "he never said" look the same:
  one reason nothing in Phase 3 may block on it. `states` is free text ("States you can deliver to").
- **2.1 bid facts**: consignee rows have **PIN, address, quantity, delivery days, page + quote, but no
  state**. Addresses rarely name the state (4 of 5 fixtures don't: "...Pandeypur Varanasi"), so 3.1 gets
  the state from the PIN. Defence bids mask the PIN (`***********AMRITSAR RURAL`).
- **2.1 gap found**: `emd_required` is NOT_FOUND on 4 of 30 corpus bids that do show an EMD amount
  (9748067, 10009049, 9781965, 9940677): in all four a page footer ("2 / 8") sits between the EMD lines
  ("/EMD Detail", "/Advisory Bank", bank name, "/EMD Amount"), which the second pattern does not allow. Today this shows
  as "Couldn't find EMD required" (a review, not wrong). **Fixed as the first part of 3.4.**
- **Not in any of the 30 bids**: item-wise evaluation (all are "Total value wise evaluation"), a Q1 or
  Q3 tag (all tagged items are Q2). **Found**: one PAC bid (9781965, Godrej furniture); GeM's own list of
  terms a buyer may not add, printed in every bid after "/Disclaimer" (14 items).

## Rules for every check

1. **BLOCKED needs all four**: the bid fact was read by code (not the AI, not a pattern sentence) and is
   FOUND with page + quote; his profile fact is one he typed (not a default, not empty); no GeM exception
   can apply; the GeM rule is in an official source (HANDOFF §4a). No Phase 3 check meets all four.
2. **Silent** when nothing relevant is asked, or when the profile part is empty and the bid asks nothing
   about it. **"Add X to your profile to check this"** only when the bid asks for X and the profile is empty.
3. **One result per thing, with its quote.** When a check takes over a clause category (3.3 takes
   `oem_authorisation`), `RestrictiveClauseRule` stops listing that category, so one quote never gives two
   reviews. Results about the same check and the same quote merge into one.
4. **Words**: what the bid asks (its words in quotes), what his profile says, what to do, where on GeM,
   by when. Never "eligible", "you will win", "guaranteed", "illegal", "invalid" (wording rules §Drafts 3).
   A GeM rule not confirmed in §4a adds "(GeM rule not confirmed; check on GeM)". Dates via `wording.deadline()`.
5. **The AI never feeds a check.** Rules see `BidAnalysis` only (code-read fields, pattern flags,
   consignees, spec rows). `ai_terms` from 2.5b are shown to him, never checked.
6. **Only the bid PDF.** Checks don't see the attached ATC file's text; `UnreadAttachmentRule` already tells
   him to read it, and the 2.4 checklist lists what it asks.
7. Verdicts are worked out on every read (`BidQueryService`), so a rule change needs no re-read. A new
   **clause pattern** changes the stored flags: bump `PARSER_VERSION` in that step.

## 3.1 Delivery state (`DeliveryStateRule`)

Reads `bid.consignees` (PIN, address, quote), `profile.states`, and a new clause pattern
`local_presence` (buyer section only): "office ... (located|registered) in the (state|city) ...",
"service centre in the state of ...". Real: 10044495 "An office of the Service Provider must be located in
the state of Consignee."; 10018043 "Office registered in the city of Visakhapatnam is mandatory."

State from PIN, by its first two digits (India Post zones). Some prefixes cover more than one state; the
check uses the whole set:

| PIN starts | State(s) | PIN starts | State(s) |
|---|---|---|---|
| 11 | Delhi | 49 | Chhattisgarh |
| 12, 13 | Haryana | 50 | Telangana |
| 14, 15 | Punjab | 51, 52 | Andhra Pradesh |
| 16 | Punjab, Chandigarh | 53 | Andhra Pradesh, Puducherry |
| 17 | Himachal Pradesh | 56-59 | Karnataka |
| 18 | Jammu and Kashmir | 60 | Tamil Nadu, Puducherry |
| 19 | Jammu and Kashmir, Ladakh | 61-64 | Tamil Nadu |
| 20-23, 25, 27, 28 | Uttar Pradesh | 67 | Kerala, Puducherry |
| 24, 26 | Uttar Pradesh, Uttarakhand | 68 | Kerala, Lakshadweep |
| 30-34 | Rajasthan | 69 | Kerala |
| 36, 39 | Gujarat, Dadra and Nagar Haveli and Daman and Diu | 70-72 | West Bengal |
| 37, 38 | Gujarat | 73 | West Bengal, Sikkim |
| 40 | Maharashtra, Goa | 74 | West Bengal, Andaman and Nicobar |
| 41-44 | Maharashtra | 75-77 | Odisha |
| 45-48 | Madhya Pradesh | 78 | Assam |
| 80, 84, 85 | Bihar | 79 | Arunachal Pradesh, Manipur, Meghalaya, Mizoram, Nagaland, Tripura |
| 81-83 | Bihar, Jharkhand | 90-99, other | unknown (Army Post Office) |

Profile names are matched to these names with a short alias list (UP, MP, AP, J&K, Delhi/NCT, Orissa,
Pondicherry...). A profile state no alias knows is shown as a profile warning, not guessed. Checked in 3.1
on the corpus PINs whose address names a city (Nashik 422 Maharashtra, Varanasi 221 UP, Udaipur 313
Rajasthan, Hubli 580 Karnataka).

| Case | Outcome | Words (shape) |
|---|---|---|
| `profile.states` empty, or no consignee rows (services) | silent | |
| every row's state set is inside his states | silent | |
| a state set has nothing in common with his states | REVIEW, one per state, quote of its first row | "Delivery to Karnataka (Hubli, 4 rows, 4 units): not one of the states you deliver to. Price the freight to the consignee, or skip." |
| a state set only partly overlaps (e.g. 24 → UP or Uttarakhand) | REVIEW | "Delivery to PIN 248001 (Uttar Pradesh or Uttarakhand): check it is a state you deliver to." |
| PIN masked or unknown prefix | REVIEW, one for all such rows | "Delivery place masked by the buyer: AMRITSAR RURAL (9 rows). Check its state." |
| `local_presence` flag | REVIEW with quote (even if `states` is empty) | "The buyer asks for a local office: “…”. Check you have one there." |

Never BLOCKED: "states you deliver to" is his preference; he can still choose to deliver.

## 3.2 Certificates (`CertificateRule`)

Reads `documents_required` entries and `certification` clause flags; pulls out named standards by code:
`ISO 9001`, `ISO 14001`, `ISO/IEC 27001`..., `BIS`, `IS 8126`... (normalised: case, spaces, ":2015" year
dropped). Compares with `profile.certifications` normalised the same way. **By number**: today's
shortfall check counts any "ISO" in the profile as covering "ISO 14001"; 3.2 must not.
"Certificate (Requested in ATC)" slots are left to the 2.4 checklist (no number to check).
An `IS nnnn` inside the item name ("Composite Office Tables conforming to IS 8126") is a product standard
the maker holds: REVIEW only if he is the OEM of that item, else silent.

| Case | Outcome | Words |
|---|---|---|
| no named standard asked | silent | |
| asked, in his profile | silent | |
| asked, profile certifications empty | REVIEW (one, listing all) | "The bid asks for ISO 9001, BIS (page 3: “…”). Add your certificates to the profile to check them." |
| asked, not in his non-empty list | REVIEW per standard | "The bid asks for ISO 14001 (page 3: “…”); your profile lists ISO 9001. Attach it if you have it, or skip." |

Never BLOCKED: the list is free text he may not have finished, and some certificates are the maker's.

## 3.3 OEM, authorisation, OEM turnover (`OemRule`)

Reads `documents_required` entries "OEM Authorization Certificate" and "OEM Annual Turnover" (seen in 12
of 30 bids), `oem_authorisation` flags (takes the category over from `RestrictiveClauseRule`), the quadrant
tag in `item_category` ("(Q2)"), `profile.is_oem`, `oem_products`, `categories`.

He is the **maker of this bid's item** when `is_oem` and (`oem_products` empty, or `item_match` of
`item_category` against `oem_products` hits). Otherwise he is a reseller for this bid.

| Case | Outcome | Words |
|---|---|---|
| he is the maker of the item | silent | |
| reseller; OEM authorisation asked (form entry or flag) or item tagged Q2 | REVIEW, one result | "The bid asks for an OEM authorisation certificate (page 2: “…”). As a reseller, get one from the maker of the product you offer before the bid closes ({deadline})." |
| reseller; OEM Annual Turnover asked | REVIEW (merged into the result above when both) | "...and the maker's turnover certificate (CA certified)." |
| reseller; item tagged Q1 | REVIEW | "GeM lists this item in Q1: only its maker (OEM) can offer it. Your profile says you are not the OEM of it. (GeM rule not confirmed; check on GeM)" |

Never BLOCKED: `is_oem` cannot tell "no" from "not answered", and resellers get authorisations routinely.

## 3.4 EMD (`EmdRule`, replaces today's)

First: fix `emd_required` (footer line between labels; amount after "/Advisory Bank" means required) on a
fixture copy of 9748067, and treat a FOUND `emd_amount` > 0 as required. Bump `PARSER_VERSION`.
Reads `emd_required`, `emd_amount`, `estimated_bid_value`, `item_category`, `bid_end`, `profile.is_mse`,
`is_startup`, `own_made_products`, and a new clause pattern `emd_state_limit` (buyer section):
MSE exemption limited to sellers of a state ([GTC] cl. 4(m) allows this only in the ATC).
"Makes the item" = `item_match(item_category, own_made_products)` hits.

| Case | Outcome | Words |
|---|---|---|
| no EMD | silent | |
| EMD asked, estimated value FOUND below ₹5,00,000 | REVIEW | "This bid asks an EMD of ₹Y, but its estimated value is ₹X (below ₹5 lakh); GeM's terms say no EMD below ₹5 lakh. You may ask the buyer through a representation by {date}." |
| EMD asked; MSE and makes the item, or startup | REVIEW | "EMD ₹X: you may be exempt (MSE making this item / DPIIT startup). Claim it with your Udyam / DPIIT certificate when you bid." + `emd_state_limit` quote when present |
| EMD asked; MSE, `own_made_products` empty | REVIEW | "EMD ₹X. MSEs are exempt only for items they make; add the items you make to your profile to check." |
| EMD asked; MSE but resells this item | REVIEW | "EMD ₹X: the MSE exemption covers only items you make, so pay it before the bid closes ({deadline})." |
| EMD asked; not MSE or startup | REVIEW | "Pay an EMD of ₹X before the bid closes ({deadline})." |

Never BLOCKED: paying EMD is a step, not a bar.

## 3.5 Exact specification (`SpecMatchRule`, needs 3.9; build 3.9 first)

Reads `bid.specifications` and his products' key specs (3.9). Only products whose name `item_match`es
`item_category`. Spec rows have no item number; a new table starts where a spec name repeats (the cartridge
bid 10014519 has 4 tables, one per colour). Names compared normalised (case, spaces, punctuation).
Allowed values: comma-separated list, or "a to b" bands with "Or higher" on the last one (numbers).

| Case | Outcome | Words |
|---|---|---|
| no 3.9 product matches the item, or no spec rows | silent | |
| some table has no mismatch on the names both sides have | silent | |
| every table has a mismatch | REVIEW, quoting the closest table's first mismatch | "Your product “Canon PFI-8110 BK” has Color = Black; this bid allows only Magenta (page 4: “…”). Offer a product that matches exactly." |
| a value he gave can't be compared (text vs band) | silent, listed under the bid's spec rows as "not compared" | |

Never BLOCKED: his 5 products are not his whole catalogue; he may source another.

## 3.6 Item-wise vs total-value (`CategoryMatchRule`, extended)

Total-value with only some items his: exists today (REVIEW "you must quote for all N items"). Item-wise:
silent in the verdict; the matching items are listed on the bid page. **No item-wise bid in the corpus**:
3.6 starts by finding one through the app (a discovery search; one listing page, one PDF) and saving it as
the fixture. Until then it stays unbuilt.

## 3.7 PAC: fixed make or model (`PacRule`)

Reads a new clause pattern `pac` (buyer section, or the MII-waiver text in the bid form): "PAC mode",
"PAC Bidding", "Proprietary Article Certificate" — but not GeM's standard sentences ("except in case of
Single Bid / Proprietary Article Certificate (PAC) Buying", the cartridge note "such PAC may not be
required"), added to `GEM_STANDARD_WORDING`. Real: 9781965 "...in the bids floated on GeM Portal under
PAC Bidding." and "Since the procurement is based on PAC mode...".

| Case | Outcome | Words |
|---|---|---|
| no PAC sentence | silent | |
| PAC sentence | REVIEW with quote | "This is a PAC bid: only the named make can be offered (page 46: “…”). Bid only if you sell that make, with the maker's authorisation." |

Never BLOCKED: the profile has no list of makes he is authorised for.

## 3.8 Terms GeM does not allow (`ForbiddenTermRule`)

Every bid prints GeM's list (after "/Disclaimer") of buyer terms that make the bid "null & void". The
scanner's buyer section ends exactly there, so the list itself is never flagged. New clause patterns, one
category each, for the items code can spot (each REVIEW wording is "may", since a pattern can't be sure):

| GeM item | Category | Looks for |
|---|---|---|
| 2 brand / make mandated (not in PAC bids) | `forbidden_brand` | "(make|brand) ... only", "of make X only" |
| 4 paper documents before qualifying (EMD and integrity pact allowed) | `forbidden_physical` | "hard copy", "physical copy/form", "sealed envelope/cover", "by post/courier"; not when the sentence names EMD or integrity pact |
| 7 samples with the bid | `forbidden_sample` | "sample(s)" with submit / along with / before / approval |
| 8 experience only from a named organisation, or foreign/export | `forbidden_experience` | "experience ... (only|exclusively) ... (department|organisation|ministry|PSU ...)", "export/foreign experience" |
| 10 terms on an outside website or document | `forbidden_external` | a link not on gem.gov.in, "available on (the) website" |
| 11 tender fee / participation fee | `forbidden_fee` | "tender/bid/document fee or cost", "participation fee", "processing fee" |

Items 1, 3, 5, 6, 9, 12-14 need judgment: not checked (the AI reading may show them).

Representation deadline ([SFAQ], bid start = `bid_dated`): bid open 10+ days → start + 4 days; 6-9 days →
+2; 3-5 days → +1; end of that day. Only once per bid.

| Case | Outcome | Words |
|---|---|---|
| no such flag | silent | |
| flag, window open | REVIEW per flag | "This term may be one GeM does not let buyers add (GeM's list in this bid, item 11: “Asking for any Tender fee…”): “{buyer quote}”. You can ask the buyer to remove it: Bids → {bid} → Create representation, {deadline}. Only one representation per bid." |
| flag, window passed | REVIEW | same, ending "The time to ask the buyer has passed ({missed date}); bid on the terms as written, or skip." |
| `bid_dated` not found | REVIEW | same, with "date unknown; check on GeM" |

Never BLOCKED: a forbidden term is the buyer's mistake, not his.

## 3.9 Main products with key specs (profile, if D4 = yes)

Profile gets `products`: up to 5, each a name and up to 15 "spec name = value" pairs. Spec names are picked
from names seen in stored bids' spec rows (so they match GeM's words), or typed. Stays on this computer;
goes to Groq only when he asks the chat about it (build rule 6). No check of its own; 3.5 uses it.

## Build order and size

3.1, 3.2, 3.3, 3.4, 3.7, 3.8 can go in any order (each one class + patterns + table tests on real
sentences). **3.9 before 3.5. 3.6 waits for an item-wise fixture.** Each step adds its row to `done-log.md`.
