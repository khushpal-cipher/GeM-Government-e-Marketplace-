# Handoff: where we stopped (19 Oct 2026)

Read this first in a new session. It records what was looked at, decided and made, so work
continues without redoing it. No code was changed in this session.

## 1. What GeM Assistant is today (from reading the whole repo)

A chat (Groq) in front of a fixed pipeline, for one GeM seller. It never logs in to GeM.

**Built:**
- Profile from chat (products, turnover, experience, MSE/startup/OEM), saved only on his Confirm.
- Search of GeM's public bid list by keyword. Limits: 5 keywords × 2 pages, 5 PDF downloads per search,
  15 min between searches, 250 GeM requests/day.
- Reads about 26 fields from the bid PDF, each with page + quote: deadline, EMD (+ amount), ePBG,
  min turnover, min experience, MSE/startup relaxations, MII, evaluation method, quantity, ministry.
- Verdict per bid: ELIGIBLE / NEEDS_REVIEW / BLOCKED (`eligibility/rules.py`).
- Keyword flags on buyer clauses (`parsing/clause_patterns.py`); corrigendum fetched and shown as raw text.
- Add a bid from a pasted GeM link; safety stop on any block page.

**Not yet verified:** chat never run against real Groq; website mode never deployed.

**Gaps found in code:**
- `profile.states`, `certifications`, `is_oem` are saved but no rule uses them; chat can't set states/certificates.
- Product match is literal words ("office chair" misses "Revolving Chair"); no GeM filters used.
- No scheduled search, no alerts, no Excel export.
- Buyer's attached ATC file is never read (only "open it yourself"); spec file not read.
- Consignee (delivery address) not extracted.

## 2. What can be automated next (agreed list)

Can be fully automated, not built yet:
daily search; "new since last time"; GeM category names; GeM filters (state, type, ministry, date);
alerts (WhatsApp/SMS/email); read the attached ATC file; AI reading of buyer clauses with quotes;
read spec file; corrigendum summary; read delivery address; check delivery state, certificates,
OEM authorisation, MSE EMD exemption; flag terms GeM forbids; document checklist; Excel report;
past winning (L1) prices; order/payment reminder tracker.

AI can prepare only (he acts): pre-bid questions and complaints (drafts), price-range advice.

Never automate (needs his login / legal liability): login, catalogue, bid submission, EMD/ePBG
payment, reverse auction, accepting orders, invoices, vendor assessment.

**Suggested build order:** 1) read attached ATC file, 2) early alerts for new bids,
3) delivery-state + exact-spec + certificate/OEM checks + document checklist, 4) past L1 prices.

## 3. Pitch deck (made)

12-slide pitch, written as if section 2 is all built:
https://claude.ai/artifact/9VDUKAYumgfxfme7ZpUDrQ (private until shared from its Share menu).
To fill: `[Your name]`, `[Date]`, pilot size `[__]` sellers / `[__]` weeks, `[Your ask]`, contact.

## 4. GeM training playlist (read)

Playlist: https://youtube.com/playlist?list=PLffbgSv9050j2xxXP117UIAt3dkJszQBz (15 videos, ~4 h,
Rohit Semwal, 2024). Read from Hindi auto-captions only (not watched). Re-fetch captions with:
`uvx yt-dlp --skip-download --write-auto-subs --sub-langs hi --sub-format vtt <playlist url>`.

What a seller does, by stage (V = video number):

- **Registration (V2):** sign up as seller (free); docs: Aadhaar + linked phone, email, business PAN,
  bank + IFSC, 3 yrs ITR, address (GST optional); Aadhaar + email OTP; profile: PAN, start date,
  office, bank, ITR if business > 2 yrs ("revenue from operations"), e-invoicing if turnover > ₹5 cr,
  Udyam (same phone), startup only with DPIIT certificate, no-China declaration; caution money
  ₹5k (≤₹1 cr) / ₹10k (₹1–10 cr) / ₹25k (>₹10 cr), refundable, waived for women and SC/ST MSEs.
- **Account (V4):** up to 50 secondary users with roles (one login = one session); close account.
- **OEM (V7):** everyone starts as reseller; vendor assessment by RITES (desktop docs + geo-tagged
  video); exemptions (₹500 cr turnover, BIS, drug licence, PSU/govt); deemed OEM, third-party maker;
  trademark → instant listing approval, else affidavit brand or "Unbranded – company".
- **Quadrants (V3):** Q1 OEM only; Q2 OEM + authorised resellers; Q3 anyone incl. unbranded until the
  brand's OEM joins; Q4 open. Category search tips (V4): try synonyms, "Browse all categories".
- **Products (V5, V6):** "Sell this item" copy (Q3/Q4, Q2 with authorisation); offer ≥10% below MRP,
  within category price range; states/districts, stock, min order, delivery days (buyers give ≥15);
  MRP change request with proof; "View all sellers" shows prices by location; new listing with
  dropdown specs, MRP proof, 3 matching photos, admin approval; published listings can't be edited
  (re-upload using "Clone catalogue specification"); brand approval needs a registered trademark.
- **Services (V8):** list instantly; some need licences (food for catering, labour for manpower,
  PSARA for security); no category on GeM = can't list.
- **Finding bids (V9):** bid types: product, service, bid-to-RA (lowest 50% or highest-one-eliminated),
  custom (no category, ≥21 days), BOQ (≥5 items without category), bunch, PAC (fixed brand/model);
  logged out: advance search by category+date, ministry, consignee city, BOQ title; logged in: only
  bids for categories in his catalogue.
- **Bidding (V10–V13):** check bid validity, buyer vs **consignee** (price freight to consignee);
  exact spec match required (listing can take up to 24 h to appear inside the bid → list early);
  all-in price; GeM charge ₹10k + GST per ₹20 lakh of orders per year, then a % on orders ≥ ₹5 lakh
  (% unclear in captions); documents: experience, past performance (% of qty or value), CA turnover
  certificate, ATC certificates, OEM authorisation + OEM turnover, MSE; 10 MB per file; ATC on terms
  link or last page of PDF; EMD before, ePBG after winning; OTP submit; withdraw/resubmit up to 3×;
  questions to buyer ("Create representation") in first 4 days, buyer must answer; item-wise
  evaluation lets him bid on some items (total-value and service bids need all); custom bid = one-off
  catalogue per bid; BOQ bid = no catalogue (make, model, HSN go on the PO).
- **Results (V15):** own results with rejection reasons; challenge within 2 days (one time);
  logged out, any bid's result (winner + price) and daily contracts/POs are public.
- **Direct purchase (V14):** ≤ ₹25k direct order; ₹25k–₹5 lakh needs 3-way comparison; to win a
  promised order, list a product with no lower price for that location and send the buyer the link.

Not covered by the playlist: accepting orders, delivery, invoices, payments, ePBG submission,
₹25k–₹5 lakh direct purchase, ratings/penalties, disputes.

**Findings for the product:** past L1 prices are public (closes the open question); alerts must be
early because listings take up to 24 h to reach a bid; price to the consignee address.

## 5. Decided next steps (not started)

1. Screen-record one real session with the seller on his own GeM account (he logs in, never share
   the password); note slowest steps and past lost bids.
2. Read GeM's official seller handbooks / SOPs / FAQs to fill the gaps in section 4 and check the
   2024 video facts against today's portal.
3. Keep one source-and-date record per fact (the architecture doc's standing rule).
4. Then build in the order in section 2.

## 6. State of the repo

Branch `docs/hinglish-testing-guide`; nothing committed this session; this file is new and uncommitted.
`.claude/` is untracked. yt-dlp is not installed (Homebrew install was stopped); use `uvx yt-dlp`.
