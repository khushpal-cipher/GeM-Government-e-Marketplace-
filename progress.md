# Progress: GeM Assistant

Every session reads this file first and updates it before the session ends.
Details live in `docs/HANDOFF.md`; this file only says what is done, what is next, and where to continue.

## Rules (from the owner)

- Commit only on this computer. **Never push or open a PR**: a friend is changing the GitHub repo.
- Don't redo work listed under "Done".
- Explain things in simple words.
- **Update this file before the session ends**: move finished items to "Done", rewrite "Continue from here",
  add the date. Then commit it locally.
- When the owner types **"give me a prompt"**: update this file and `docs/NEXT_SESSION_PROMPT.md`,
  commit locally, and reply with the "Prompt to paste" box from that file.

## Done

| Date | What | Where |
|---|---|---|
| 19 Oct 2026 | Read the whole repo; list of gaps in the code | HANDOFF.md §1 |
| 19 Oct 2026 | Agreed list of what AI can automate, and build order | HANDOFF.md §2 |
| 19 Oct 2026 | 12-slide pitch deck (private artifact) | HANDOFF.md §3 |
| 19 Oct 2026 | Read the 15-video GeM training playlist from **captions only** → seller task list | HANDOFF.md §4 |
| 19 Oct 2026 | Read GeM's official rules (GTC v1.29 of 25 Mar 2026, FAQs, penalty policy): orders, ePBG, delivery, invoices, payment, penalties, disputes; 2024 video facts checked | HANDOFF.md §4a |
| 20 Oct 2026 | Full seller process table: what AI can do fully / prepare only / never (given in chat; matches §2) | HANDOFF.md §2 |
| 20 Oct 2026 | Tested that the built-in browser can play the videos and screenshot frames (works; ads need skipping) | — |
| 20 Oct 2026 | Watched all 15 training videos ("Option A"): frames at each screen change + Hindi captions; screen-by-screen notes, what changed since 2024, AI level per screen, and a product summary at the end | docs/gem-videos.md |
| 20 Oct 2026 | Decided: **no logging in or scraping GeM with a bot** (grave-penalty risk). A later live tour is read-only, the owner logs in himself, human speed, no submit/accept/pay clicks | — |
| 20 Oct 2026 | Full build plan for everything on top of the current app (below, "Build plan") | progress.md |
| 20 Oct 2026 | Live read-only tour of the seller's own GeM account (step 8.0): owner logged in himself in his Chrome; dashboard, orders, shipment/CRAC/payment, participated bids, clarification history, incidents. New steps 4.5, 5.0, 7.6 added | docs/live-tour.md |
| 20 Oct 2026 | FINAL build plan from videos + live tour (replaces the first plan; Phase 1 = paste-in daily check, shortfall helper, order tracker) | progress.md |

## Which model to use (owner switches it in the app's model picker)

Default: **Sonnet · Medium**. Before starting each step, Claude tells the owner in one line if he must switch.

| Steps | Model · Effort |
|---|---|
| 0.3, 1.0, 2.5a, 2.5b, 3.0, 8.2 | **Switch to Opus · High**, switch back to Sonnet after the step |
| 2.1 | Sonnet · **High** (money and quantity parsing) |
| 0.1 | Sonnet · Low |
| 2.7, 4.3, 5.3 | Haiku · Low (or just stay on Sonnet) |
| everything else | Sonnet · Medium |

## Continue from here (written 20 Oct 2026)

State: code unchanged since `ca5a4b1`; `cd backend && uv run pytest -q` → **398 passed** (20 Oct 2026).
**FINAL build plan written 20 Oct 2026 (below, commit 356ce01). Owner said start building (20 Oct 2026).** Nothing in it is started yet.

**Next exact action:** start **step 0.1** (chat against real Groq: the key is already in
`~/Library/Application Support/GeM Assistant/.env`), then **1.0**. Steps 0.2/0.3 wait for D2 (contact email).

## Build plan (FINAL, written 20 Oct 2026, approved by the owner 20 Oct 2026, nothing started)

**Goal:** the app does everything in HANDOFF §2 "fully automated" and "AI prepares", sharpened by
`docs/gem-videos.md` and `docs/live-tour.md`. Still never: login, captcha, OTP, submitting, paying, accepting.

**What changed from the first plan, and why**
1. **New Phase 1 "Don't miss what's waiting in his account" comes first.** The live tour found a buyer's
   shortfall request sitting unanswered on the logged-in "Already participated" page, an order pending
   acceptance, and shipments with CRAC but "Payment not generated yet". These cost him money today and
   need **no GeM requests**: he pastes, the app tracks and reminds. Cheapest, safest, fastest value.
2. **Profile additions moved up** (old 2.1 → 1.1): the shortfall helper and every later check need them.
3. **Rejection reasons + challenge draft moved up** (old 7.4 → 1.5): half his recent lost bids were lost
   on technical grounds (dashboard "lost financial vs technical"); 48 h window.
4. **Order tracker moved up** (old 8.1 → 1.4), with stages and dates now fixed from the live screens:
   Contract Placed → Dispatched (invoice **before the expected delivery date**, else the order expires) →
   Received (CRAC date) → Payment (due CRAC + 10 days). Adds the GeM charges calculator.
5. **Invited-bid import** (4.5) and **daily check card** (5.0) from the live tour are in Phase 1.
6. **Recon (0.3) gets the live-tour questions:** result pages whose evaluation didn't open, whether the
   buyer Red/Orange flag or PBP notices are public. D1 (Groq key) is **done**: the key is in `.env`.
7. "Read the whole bid" and the checks stay the core (Phases 2–3), unchanged in substance.
8. New small steps from the videos: buyer payment flag on each bid (2.7, if public), direct-order
   price check per location (6.3), PBP alert (4.6, if public).

### How every step is built

1. Write a failing test first, on a saved real fixture (PDF / JSON / HTML / pasted text). Make it pass.
   Run the whole suite. Commit locally. Update this file (Done row with commit hash, next action).
2. **Every GeM request goes through `SafeFetcher`** (URL policy, 4 s gap, 250/day, breaker). No new
   POST paths, no new hosts outside `*.gem.gov.in`, without asking the owner.
3. **A new GeM page type is looked at before code** (recon): robots.txt of that host, one request by
   hand-speed, saved as a fixture, written down with the date in `docs/02-RECON-FINDINGS.md` (created by 0.3).
4. Bump `PARSER_VERSION` whenever field rules / patterns / checks change, so stored bids are re-read.
5. The LLM only finds and quotes. A value the LLM gives is kept **only if its quote is found word for
   word in the document**; numbers are re-read from the quote by code. Deterministic rules decide.
6. **Pasted text from his GeM account is his own data**: it stays on this computer, is never sent to GeM,
   and goes to Groq only when he asks the chat about it (same rule as the profile today).
7. Daily GeM request budget after all steps (limit 250): 2 scheduled searches × (10 listing pages +
   5 PDFs + 5 corrigenda + up to 10 attached files) ≈ 60, invited bids ≤ 10 × 2 = 20, past results ≤ 10,
   category look-ups ≈ 5 → **≈ 95/day**. A step that would push this past ~150 needs the owner's OK.

Annotation per step (owner's rule): `→ Model · Effort · Why`.

### Decisions for the owner (default used if he doesn't answer)

| # | Question | Default |
|---|---|---|
| D1 | Groq API key | **Done 20 Oct 2026**: in `~/Library/Application Support/GeM Assistant/.env`, accepted by Groq |
| D2 | Which email GeM sees on every request (the app won't contact GeM without one) | **Still needed** for 0.2, 0.3, 4.x, 6.x; Phase 1 needs none |
| D3 | How alerts reach him: in-app + Mac notification (free) / email (free, Gmail "app password") / WhatsApp (paid) | In-app + Mac notification; email next; WhatsApp only if he asks and pays |
| D4 | Will he type the key specs of his main products (e.g. "A4, 80 GSM") for exact-spec checks? | Yes, up to 5 products; without it 3.5 is skipped |
| D5 | One seller (his father) or several (a pilot)? | One seller until the pilot |
| D6 | Put the website online (Fly.io Mumbai, card needed, ~₹0–500/month) or stay on the Mac app? | Mac app until Phase 5 is done |
| D7 | New real bid PDFs as test fixtures hold officers' names/phones. Commit them? | Commit only the few each test needs |

### Phase 0 — Prove what exists, collect real documents

- **0.1** Run the chat against real Groq with `docs/testing-hinglish.md`; fix what breaks. D1 done.
  → Sonnet · Low · scripted guide exists; mostly running and reading output.
- **0.2** One `corpus` run (30 varied bid PDFs: product, service, custom, BOQ, PAC, item-wise, bid-to-RA)
  + `probe`. Pick fixtures for Phases 2–3 (none of the 4 current ones shows "Delivery Days" in plain text). Needs D2.
  → Sonnet · Medium · guarded commands exist; picking a varied set needs judgment.
- **0.3** Recon, read-only, hand speed, into `docs/02-RECON-FINDINGS.md`: robots.txt of
  `fulfilment.gem.gov.in`; the text ATC page `contract/terms.jsp?bidra=`; one buyer ATC file, one spec PDF,
  one BOQ detail file (PDF/XLSX?); two finished bids' `getBidResultView` (are prices filled in? the tour's
  sample didn't open); `/all-bids` filters (bid type, status, end date) and `/advance-search` (consignee
  state, BOQ title); `mkp.gem.gov.in/search?q=`; a product's "Other Sellers" page; is the buyer Red/Orange
  flag or a PBP notice anywhere public. Needs D2.
  → Opus · High · every later phase is built on these findings; a wrong one poisons them all.

### Phase 1 — Don't miss what's waiting in his account (no GeM requests; he pastes, the app never logs in)

- **1.0** Wording rules for everything the app drafts or reminds (always "draft — check before sending";
  never says "submit/accept for you"; how deadlines are phrased; Hinglish tone).
  → Opus · High · drafts go to government buyers under his name.
- **1.1** Profile gets: states he can deliver to, certificates held, OEM or reseller (per product), "do
  you make this item yourself" (MSE EMD exemption), Udyam, DPIIT, years in business, ITR filed on GeM,
  PFMS-verified bank. Chat proposes, he Confirms. Onboarding warnings (e.g. >24 months old and no ITR on
  GeM = can't bid). Files: `domain/models.py`, `infrastructure/database.py` (migration),
  `services/chat_tools.py`, `frontend/js/views/profile.js`.
  → Sonnet · Medium · model + migration + chat tool, existing pattern.
- **1.2** **Daily GeM check card** + in-app alerts list: each morning the app asks him to open *Bids →
  List of Bids → Already participated* and the dashboard, and paste: pending clarifications (bid no, text,
  last date), orders pending acceptance, orders near expected delivery date, CRACs without payment, open
  SCNs. Parsed by code (bid numbers, dates); anything unclear is shown back for him to fix. Each item
  becomes an alert with its due date (clarification last date; 120 h acceptance; SCN 10 days).
  → Sonnet · Medium · new table + form + chat card; parsing pasted text needs care.
- **1.3** **Shortfall-reply helper**: from a pasted clarification, list each document asked (OEM
  turnover 3 yrs, OEM authorisation…), mark which his profile says he has, draft the covering note (1.0
  rules). He uploads and submits himself.
  → Sonnet · Medium · deterministic document patterns first; depends on 1.0 + 1.1.
- **1.4** **Order tracker**: he pastes the order details (or types contract no, date, value, expected
  delivery date, ePBG %). Stages Contract Placed → Dispatched → Received (CRAC) → Payment. Deadlines from
  HANDOFF §4a + live tour: ePBG 15 days; **invoice before expected delivery date or the order expires**;
  LD 0.5%/week late (max 5%/10%); buyer request 5 days; CRAC 10 days after proof of delivery; payment
  10 days after CRAC → "late since <date>: raise 'delay in payment' incident" with draft text. GeM charges
  calculator (₹10k + GST at ₹20 lakh/year; 0.30% on orders > ₹10 lakh, max ₹3 lakh).
  → Sonnet · Medium · date arithmetic from written rules; table-driven tests for every deadline.
- **1.5** **Rejection reason reader + challenge draft**: he pastes the buyer's disqualification reason;
  the app names the missing document, checks it against the profile, drafts the one-time challenge with
  the 48 h deadline, and remembers the reason so future checklists warn earlier.
  → Sonnet · Medium · reuses 1.3 patterns and 1.0 rules.
- **1.6** **Import invited bids** (old 4.5): he pastes "You are invited to participate in bid (GEM/…)"
  lines; the app finds each bid's document id with one listing search per bid number (existing guards,
  ≤ 10 a day) and analyses it. Needs D2 only for the lookup; the paste/parse part is built first.
  → Sonnet · Medium · bid number → doc id through existing `SafeFetcher` paths only.

### Phase 2 — Read the whole bid (the core value)

- **2.1** New fields from the bid PDF, each with page + quote: consignee rows (address, state, quantity,
  **delivery days**), estimated bid value, inspection required, ePBG duration (months), item-wise
  schedules, PAC items (fixed make/model), past-performance %, technical-clarification days, "documents
  required from seller", links to spec / BOQ / buyer-ATC files. `sum(consignee qty) == total` else
  CONFLICTING. Files: `parsing/field_rules.py` (+ small table reader), `tests/test_parsing.py`.
  → Sonnet · **High** · money/quantity parsing; a 10× error is the worst bug.
- **2.2** Specification table per item ("Specification / Bid Requirement (Allowed Values)") as rows with page + quote.
  → Sonnet · Medium · messy pypdf table text; care, not design.
- **2.3** Download the files the bid PDF links to (buyer ATC file, spec PDF, BOQ detail), only those
  links, via `SafeFetcher`, size/page caps, stored by hash, ≤ 3 per bid, in the budget. PDF text only;
  scanned or non-PDF → "open it yourself". Depends on 0.3.
  → Sonnet · Medium · security-relevant fetching, guards already exist.
- **2.4** **Per-bid document checklist** from text ATC + attached files: each required document with
  page + quote, plus "PDF ≤10 MB and ≤100 pages each; merge ATC certificates into one PDF"; marks what his
  profile says he has and what past rejections (1.5) missed. Deterministic patterns first. Chat card.
  → Sonnet · Medium · extends the pattern engine; wording matters to him.
- **2.5a** Design the LLM reading of ATC: JSON schema, prompt, quote check, what goes to Groq (public bid
  text only), cost cap, failure → "not read, check yourself". Injection test set written first.
  → Opus · High · the highest-risk part of the system (untrusted text into a model).
- **2.5b** Build it: Groq call with no tools, schema-locked; drop items whose quote isn't in the text;
  numbers re-read by code; injection tests pass before it is switched on.
  → Opus · High · security-sensitive; re-verify 2.5a before coding.
- **2.6** Corrigendum: keep the verbatim text; add an LLM summary under the same quote rule.
  → Sonnet · Medium · reuses 2.5b.
- **2.7** Buyer payment flag (Red/Orange) on each bid: read it if 0.3 finds it public; otherwise he can
  note it from the participation page and it shows on the bid.
  → Haiku · Low · one field or one note.

### Phase 3 — Checks (each a new class in `eligibility/rules.py`)

- **3.0** Write down each rule's inputs, BLOCK vs REVIEW thresholds, and wording before coding.
  → Opus · High · decides when the app says "blocked"; a wrong block hides a winnable bid. Depends on 1.1 + 2.1; re-verify them first.
- **3.1** Delivery state: consignee states vs his states.
- **3.2** Certificates: asked (field + checklist) vs held.
- **3.3** OEM / authorisation / OEM turnover asked and he is a reseller → review with quote.
- **3.4** EMD: none below ₹5 lakh; MSE exemption only if he makes the item; ATC limiting it to the buyer's state.
- **3.5** Exact spec: allowed values vs his product specs (only with 3.9).
- **3.6** Item-wise bids: which schedules he can bid on; total-value bids: he must quote every item.
- **3.7** PAC items: only the named make/model can bid.
- **3.8** Terms GeM forbids in ATC (GTC list) → "you may ask the buyer (representation)" + last date.
- **3.9** Main products with key specs (only if D4 = yes).
  → 3.1–3.9: Sonnet · Medium · one small rule class + table-driven tests each, design fixed in 3.0.

### Phase 4 — Find bids better and earlier (needs D2)

- **4.1** GeM category names + quadrant from `mkp.gem.gov.in/search?q=`; he confirms; extra search words;
  quadrant warning (Q1 OEM only, Q2 needs authorisation). Depends on 0.3.
  → Sonnet · Medium · one new public page type behind existing guards.
- **4.2** Listing filters: bid type (BOQ / custom / service), end-date range; BOQ title and consignee
  state via Advance Search (logged-out page). Only through the page's own search. Depends on 0.3.
  → Sonnet · Medium · touches the browser search, which must stay within the safety rules.
- **4.3** "New since last search" on bids and in chat.
  → Haiku · Low · a stored first-seen time already exists.
- **4.4** Scheduled search inside the running server (e.g. 9:00 and 15:00), respecting 15 min, 5×2 pages,
  250/day and the breaker; one at a time; skipped while stopped.
  → Sonnet · Medium · background timing; must not double-run.
- **4.6** PBP notice alert, only if 0.3 finds the notice list public.
  → Sonnet · Low · small; may be dropped.

### Phase 5 — Tell him in time

- **5.1** Bid alerts in the Phase 1 alerts list: new matching bids; closing in 3 days; representation
  window closing; "list your matching product 2+ days before the bid ends" (approval can take 48 h).
  → Sonnet · Medium · reuses the 1.2 table.
- **5.2** Outbound alerts per D3 (Mac notification first). Outbound only, never commands coming in.
  → Sonnet · Medium · small adapter; secrets in the data folder like the Groq key.
- **5.3** Export bids + verdicts + checklist + open orders as CSV (opens in Excel; stdlib csv).
  → Haiku · Low.

### Phase 6 — Prices and competitors (needs D2)

- **6.1** Finished bids with his products: read the public result page (bidders, qualified or not, prices,
  L1), ≤ 10 a day. Depends on 0.3. `view_contracts` has a captcha: never.
  → Sonnet · Medium · new public page type behind existing guards.
- **6.2** Past L1 prices for similar items on a bid and in chat; advice only.
  → Sonnet · Medium · display + matching by item words.
- **6.3** Direct-order check (video 14): given category, spec, buyer's district/state and target price,
  read the product's public "Other Sellers" page and say if anyone lists lower for that location, and
  the lowest he can list (MRP − 10%). He lists and sends the link himself. ≤ 5 pages per check.
  → Sonnet · Medium · new public page type; read-only.

### Phase 7 — Drafts he checks and sends himself (chat tools; the app never sends)

- **7.1** Representation (pre-bid question) for flagged/forbidden clauses, with the last date.
- **7.2** Compliance sheet for custom bids (buyer's spec line → his offer → yes/no).
- **7.3** Make / Model / HSN list for BOQ bids (it goes onto the purchase order).
- **7.5** Listing pre-check (MRP −10%, 3 photos, MRP proof names this product, brand vs model).
  → 7.1–7.5: Sonnet · Medium · built on Phase 2 data and the 1.0 rules.

### Phase 8 — Use it for real

- **8.1** Put the website online if D6 = yes; first check one real search from the server.
  → Sonnet · Medium · steps are in README; GeM may refuse data-centre addresses.
- **8.2** Two-week pilot with his father: fields he corrected, bids it missed, alerts that helped, time saved.
  → Opus · High · decides what to build next or whether to continue.

Order: 0.1 → 1.0–1.6 → 2 → 3 → 4 → 5 → 6 → 7 → 8. Steps that need D2 (0.2, 0.3, 1.6 lookup, 4.x, 6.x)
wait for it; nothing in Phase 1 does. Step 2.3 and anything reading a new page type wait for 0.3.

Not opened in the live tour (accept/submit buttons): order-acceptance, ePBG and invoice-creation screens.
Still unchecked (HANDOFF §4a): Payment Escalation SOP, current penalty policy, Revenue Policy v1.5 PDF,
minimum delivery days, vendor assessment fee. 1.4 uses today's written rules and says where a rule is unchecked.

Housekeeping: videos and frames were **deleted on 20 Oct 2026** at the owner's request (~530 MB freed).
Only the 15 Hindi caption files remain in `../gem-videos/*.hi.vtt` (3 MB). To see a screen again,
re-download that one video at 480p (size check first). Frames were made with the bundled ffmpeg
(`uvx --with imageio-ffmpeg python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"`)
and `select='gt(scene,0.08)'`, keeping the last frame of each burst less than 3 s apart.

## Not verified yet

Chat never run against real Groq; website mode never deployed (HANDOFF.md §1).
