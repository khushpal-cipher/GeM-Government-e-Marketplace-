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

## 4a. Official GeM sources (read 19 Oct 2026)

Fills the gaps in section 4 and checks the 2024 video facts. Each fact has a source tag:

- **[GTC]** General Terms and Conditions on GeM 4.0, v1.29, dated 25 Mar 2026 (latest on
  https://gem.gov.in/page/gtc). PDF: https://assets-bg.gem.gov.in/resources/upload/shared_doc/gtc/new-GTC-on-1774431996.pdf
- **[SFAQ]** Seller FAQ https://gem.gov.in/userFaqs/seller (page has no date; read 19 Oct 2026).
- **[BFAQ]** Buyer FAQ https://gem.gov.in/userFaqs (no date; read 19 Oct 2026).
- **[IFAQ]** Incident FAQ https://gem.gov.in/userFaqs/incident (no date; read 19 Oct 2026).
- **[IM14]** Incident Management policy v14.1 (no date in the file; older than IFAQ, see note):
  https://assets-bg.gem.gov.in/resources/pdf/incident_management_policy_v14.1.pdf
- **[NEWS]** GeM fee cut, All India Radio, 21 Sep 2024: https://www.newsonair.gov.in/gem-cuts-transaction-charges-levied-on-sellers-service-providers-for-public-procurement/

### Video facts that have changed

| Video said (2024) | Today | Source |
|---|---|---|
| Caution money ₹5k / ₹10k / ₹25k by turnover | **Gone.** Waived for all sellers; "discontinued in 2025". Old deposits can be withdrawn (Dashboard → Manage Caution Money Account) | [GTC] cl. 27, [SFAQ] |
| Direct order up to ₹25k | Up to **₹50,000** with no comparison | [GTC] cl. 4, [BFAQ] |
| ₹25k–₹5 lakh needs 3-way comparison | **₹50k–₹10 lakh**: buy from the lowest of at least 3 OEMs/sellers (L1 purchase); above ₹10 lakh needs a bid/RA | [GTC] cl. 4, [BFAQ] |
| ₹10k + GST per ₹20 lakh of orders, then a % on orders ≥ ₹5 lakh | "Annual Milestone Charge" ₹10,000 + GST once a year when his sales cross ₹20 lakh in the financial year; then a transaction charge only on orders **above ₹10 lakh**: 0.30%, at most ₹3 lakh per order (from 9 Aug 2024). Must be paid before he can accept (direct/L1) or invoice (bid/RA). TDS 2% once charges cross ₹30k a year | [SFAQ] (Revenue Policy v1.5), [NEWS] |
| New listing takes up to 24 h to reach a bid | GeM "normally requires **48 hrs**" to approve a listing; list well before the bid closes | [GTC] cl. 4(e) |

### Video facts still true

- Up to 50 secondary users [SFAQ]. Minimum 10% discount on MRP [SFAQ]; MRP can change only 90 days
  after the last approved MRP [SFAQ].
- Questions to buyer (representation): within 4 days for bids of 10+ days; 1 day for 3–5-day bids,
  2 days for 6–9-day bids; only once per bid; buyer must answer 72 h before bid end [SFAQ].
- Challenge a technical rejection: once, within 48 hours after technical evaluation [SFAQ].
- Bid-to-RA: lowest 50% of qualified bidders (rounded up) [BFAQ].

### New facts: bidding money (EMD)

- **No EMD for bids below ₹5 lakh.** Above that the buyer sets 0.5–5% (GeM suggests 1%), valid 45 days
  past bid validity; hard copy to the buyer within 5 working days of bid opening or the bid may be rejected [GTC] cl. 4(m).
- Exempt from EMD: MSEs with Udyam that **make** the offered item; DPIIT startups; sellers with
  vendor assessment; BIS licence holders for that category; KVIC etc.; PSUs. A state buyer may limit
  the MSE exemption to its own state, but only by writing it in the ATC [GTC] cl. 4(m).
- EMD is lost if he withdraws/changes his bid during validity, gives false documents, or misses the
  ePBG deadline; GeM may also ban him for at least 3 months [GTC] cl. 4(n),(o).
- EMD comes back within 15 days of award (losers) or of ePBG receipt (winner) [GTC] cl. 4(p).
- Bid offers stay valid 15 days from bid opening unless the bid says otherwise [GTC] cl. 4(f).

### New facts: after he wins (orders)

- **Bid/RA orders are accepted automatically** — he can't decline [SFAQ].
- Direct/L1 orders are accepted automatically too, except from a "red-flag" buyer or for freight-heavy
  items: then he has **120 hours** to accept or decline, else auto-accepted. No penalty for declining a red buyer [SFAQ].
- Declining or missing a direct/L1 order sets that product's stock to 0 for 15 days [SFAQ]; more
  than 2 such cancels/declines in 30 days is a "severe" deviation [IM14].
- Buyer requests (cancel order, extend delivery): he has **5 calendar days** to answer; no answer =
  request declined and contract stays [BFAQ]. He can't invoice while such a request is pending [BFAQ].
- Buyer can cancel without his consent if the delivery period ends with no invoice, or 15 days after
  it ends if there's an invoice but no PRC [BFAQ].
- Buyer may raise quantity up to 25% (defence 50%) after the contract; extra time is at least 30 days [BFAQ].
- Buyer payment flag on the bid page: **Orange** = buyer hasn't paid 20+ orders whose CRAC is 70+
  days old; **Red** = 30+ such orders [SFAQ]. Worth showing on every bid in our app.

### New facts: ePBG (performance security)

- Only for bid/RA contracts; none for direct/L1 purchase [GTC] cl. 7.
- Buyer picks up to 5% of contract value (GFR range 3–5%); valid 2 months past all duties incl. warranty [GTC] cl. 7.
- **Submit within 15 days of the contract.** No payment until the buyer gets and verifies it [GTC] cl. 7, [SFAQ].
- Returned within 30 days after he finishes everything; forfeited if he fails the contract [GTC] cl. 7.

### New facts: delivery

- Price is "free delivery at site", loading/unloading and installation included, unless the category
  is marked freight-heavy [GTC] cl. 6, 13.
- Delivery date is "essence of the contract" [GTC] cl. 14.
- **Late delivery penalty (LD): 0.5% of the late quantity's value per week**, max 5% of contract value;
  up to 10% if very late (delay more than 25% of the delivery time) [GTC] cl. 15. Buyer may lower LD, not raise it [BFAQ].
- Force majeure: tell the buyer in writing within 10 days; after 90 days either side may end the contract [GTC] cl. 15.
- Not delivered on time → buyer can cancel the rest, keep the ePBG, lower his rating; GeM can ban him [GTC] cl. 19.
- Warranty 1 year from final acceptance by default; fix/replace defects within 7 days; spares for 3 years after warranty [GTC] cl. 10.

### New facts: receipt, invoice, payment

- Steps: he raises GeM invoice + uploads proof of delivery → consignee issues **PRC** (provisional
  receipt) → inspects within 10 days → issues **CRAC** (accepted/rejected qty) → buyer drafts bill → payment [GTC] cl. 11, 12; [BFAQ].
- If the consignee doesn't make the CRAC within 10 days of his proof of delivery, the system makes an
  **auto CRAC** accepting everything; consignee gets 3 more days to change it [BFAQ]. Auto-CRAC days
  are 10–60 depending on category, written in the contract [BFAQ].
- **The GeM invoice is not a GST invoice.** He must send a proper GST invoice with the goods [GTC] cl. 8(vi), [BFAQ].
  Only invoice no., dispatch mode and billing address can be edited; rejected qty → supplementary invoice [SFAQ].
- Rejected goods: take them back within 10 days at his cost, else storage charges or disposal [GTC] cl. 11.
- **Payment due within 10 days of CRAC + bill** (goods), or 10 days of SDAC (services, monthly bills) [GTC] cl. 12.
  Late-paying buyer organisations owe 1% interest per month [BFAQ].
- GST rate change between bid end and delivery is the buyer's cost (he must claim with proof);
  change before bid end is his cost [GTC] cl. 8.
- Unpaid after CRAC: raise an incident ("delay in payment"), then a helpdesk complaint under the
  "Payment Escalation SOP"; GeM's last step is a letter to the buyer's senior officers; after that
  wait 7 working days, then use the dispute route [SFAQ]. GeM can't help before a CRAC exists, but he
  can raise an incident for "delay in CRAC" [SFAQ]. (SOP PDF not read: https://assets-bg.gem.gov.in/resources/upload/shared_doc/updated-sop-for-public-domain_1744352876.pdf)

### New facts: penalties (incidents)

- Anyone (buyer, seller, system) can raise an incident on a bid, contract or listing. Sides have 7
  days to settle, then it can be escalated to GeM, which sends a show-cause notice [IFAQ].
- Reply to a show-cause notice in **10 calendar days** [IFAQ] (IM14 says 5 — the FAQ is newer).
  No reply = automatic action by severity [IFAQ]. After escalation he may offer to fix it within 10 days [IFAQ].
- Four levels: mild, serious, severe, grave [IFAQ]. Suspension (no new bids, no listing changes) per [IM14]:
  serious 30 days (45 for 3rd+ in 90 days); severe 45 days (60 for 3rd+ in 120 days, up to 12 months);
  grave up to 60 days (up to 90 for 3rd+ in 180 days, up to 12 months). *Check: these numbers are
  from v14.1, which may be out of date.*
- Examples [IM14]: late delivery = serious; not delivering a direct/L1 order = serious; bad quality
  ≤ ₹5 lakh = serious, > ₹5 lakh = severe; missing ePBG deadline = severe; withdrawing a bid = severe
  (≤ ₹5 lakh) or grave (> ₹5 lakh); not delivering after winning a bid > ₹5 lakh = grave; fake documents or MRP = grave.
- One person's other firms with the same PAN, and "allied firms", get the same penalty [GTC] cl. 24.
- Appeal once, within 10 calendar days, only with new evidence; fee 5% of contract value (₹1k–₹10k), refunded if he wins [IM14].
- Suspended for other reasons: listing in wrong category, no authorisation, fake/refurbished goods,
  late info updates, etc. [GTC] cl. 21. Update changed profile details within 7 days [GTC] cl. 3.

### New facts: disputes with the buyer

- Direct/L1 orders: talk for 30 days after a written notice → committee chaired by the buyer's
  primary user for 30 days → mediation/arbitration under the DoE guidelines of 3 Jun 2024 [GTC] cl. 16.
- Bid/RA: whatever method the buyer chose in the bid [GTC] cl. 16. Courts at the buyer's place; GeM is never a party [GTC] cl. 16, 17.

### Still not checked

Payment Escalation SOP (time per stage); current IM policy version and its suspension days;
Revenue Policy v1.5 PDF itself (rates above are from the FAQ and the 2024 news); minimum delivery
days (video said buyers give ≥15); 10 MB file limit; vendor assessment fee.

### What this means for the product

- Show the buyer's Orange/Red payment flag on each bid.
- Reminders he needs (all deadlines above): ePBG in 15 days; delivery date and LD per week late;
  5 days to answer buyer requests; 120 h for red-buyer orders; CRAC due 10 days after proof of delivery;
  payment due 10 days after CRAC; show-cause reply in 10 days; appeal in 10 days.
- EMD check: no EMD below ₹5 lakh; MSE exemption only if he makes the item.
- Warn before he declines/withdraws: stock frozen 15 days and possible suspension.

## 5. Decided next steps (not started)

1. Screen-record one real session with the seller on his own GeM account (he logs in, never share
   the password); note slowest steps and past lost bids.
2. ~~Read GeM's official seller handbooks / SOPs / FAQs~~ — done, see section 4a (a few items left under "Still not checked").
3. Keep one source-and-date record per fact (the architecture doc's standing rule).
4. Then build in the order in section 2.

## 6. State of the repo

Branch `docs/hinglish-testing-guide`. Section 4a added 19 Oct 2026 (committed locally, not pushed).
`.claude/` is untracked. yt-dlp is not installed (Homebrew install was stopped); use `uvx yt-dlp`.
