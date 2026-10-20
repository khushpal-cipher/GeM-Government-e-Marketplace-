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

## Continue from here (written 20 Oct 2026)

State: code unchanged since `ca5a4b1`; `cd backend && uv run pytest -q` → **398 passed** (20 Oct 2026).
The owner chose: **plan first, then build the whole thing** (20 Oct 2026). The plan is below; nothing
in it is started.

**Tour done 20 Oct 2026 (docs/live-tour.md).** **Next exact action:** make the FINAL plan (videos + live tour), show it to the owner, wait for his OK. Then: get the owner's answers to "Decisions for the owner" (below; each has a
default, so building may start without them). Then start **step 1.1** (bid-PDF fields, test-first with
the 4 fixtures already in `backend/tests/fixtures/`). Steps 0.1 and 0.2 run as soon as the owner gives
the Groq key and the contact email.

## Build plan (written 20 Oct 2026, nothing started)

**Goal:** the app does everything in HANDOFF §2 "can be fully automated" and "AI can prepare only",
sharpened by `docs/gem-videos.md` (summary at the end): find his bids early, read the **whole** bid
(PDF + buyer's ATC file + spec/BOQ files), check them against a fuller profile, give a per-bid
document checklist, warn him in time, show past winning prices, draft the texts he sends himself, and
track deadlines after he wins. Still never: login, captcha, OTP, submitting, paying, accepting.

### How every step is built

1. Write a failing test first, on a saved real fixture (PDF / JSON / HTML). Make it pass. Run the whole
   suite. Commit locally. Update this file (Done row with commit hash, next action).
2. **Every GeM request goes through `SafeFetcher`** (URL policy, 4 s gap, 250/day, breaker). No new
   POST paths, no new hosts outside `*.gem.gov.in`, without asking the owner.
3. **A new GeM page type is looked at before code** (recon): robots.txt of that host, one request by
   hand-speed, saved as a fixture, written down with the date in `docs/02-RECON-FINDINGS.md` (the
   architecture's standing rule; that file doesn't exist in this repo yet, step 0.3 creates it).
4. Bump `PARSER_VERSION` whenever field rules / patterns / checks change, so stored bids are re-read.
5. The LLM only finds and quotes. A value the LLM gives is kept **only if its quote is found word for
   word in the document**; numbers are re-read from the quote by code. Deterministic rules decide.
6. Daily GeM request budget after all steps (limit 250): 2 scheduled searches × (10 listing pages +
   5 PDFs + 5 corrigenda + up to 10 attached files) ≈ 60, past results ≤ 10, category look-ups
   ≈ 5 once per product → **≈ 75/day**. A step that would push this past ~150 needs the owner's OK.

Annotation per step (owner's rule): `→ Model · Effort · Why`.

### Decisions for the owner (default used if he doesn't answer)

| # | Question | Default |
|---|---|---|
| D1 | Groq API key for the real chat and for the LLM reading of ATC (his Groq account) | Needed for 0.1 and 1.5; until then everything else is built and tested with the scripted fake model |
| D2 | Which email GeM sees on every request (the app won't contact GeM without one) | Needed for 0.2, 6.x and any live check; nothing live until given |
| D3 | How should alerts reach him? In-app + Mac notification (free) / email (free, needs a Gmail "app password") / WhatsApp (paid, needs a Meta business account) | In-app + Mac notification first; email next; WhatsApp only if he asks and pays |
| D4 | Will he type the key specs of his main products (e.g. "A4, 80 GSM") so the app can check a bid's exact spec? | Yes, for up to 5 main products; without it, step 3.5 is skipped |
| D5 | One seller (his father) or several sellers (a pilot)? | One seller until the pilot; several sellers is a separate, big change (per-user data) |
| D6 | Put the website online now (Fly.io Mumbai: needs a Fly account + card, ~₹0–500/month) or stay on the Mac app? | Stay on the Mac app until Phase 5 is done |
| D7 | New real bid PDFs as test fixtures hold buyer officers' names/phones. Commit them like the 4 existing ones? | Commit only the few each test needs, as now |

### Phase 0 — Prove what exists, collect real documents

- **0.1** Run the chat against real Groq with `docs/testing-hinglish.md`; fix what breaks. Needs D1.
  → Sonnet · Low · scripted guide already exists; mostly running and reading output.
- **0.2** One `corpus` run (30 varied bid PDFs: product, service, custom, BOQ, PAC, item-wise, bid-to-RA)
  + `probe`. Pick fixtures for Phases 1–3 (none of the 4 current fixtures shows a "Delivery Days" label
  in plain text). Needs D2.
  → Sonnet · Medium · guarded commands exist; picking a varied fixture set needs judgment.
- **0.3** Recon notes, read-only, hand speed, into `docs/02-RECON-FINDINGS.md`: robots.txt of
  `fulfilment.gem.gov.in`; one buyer ATC file, one spec PDF, one BOQ detail file (type: PDF/XLSX?);
  one finished bid's `getBidResultView` (are prices filled in?); how `/all-bids` filters by Bid/RA
  status and bid type; `mkp.gem.gov.in/search?q=` (categories + quadrant); is the buyer Red/Orange
  payment flag anywhere public. Needs D2.
  → Opus · High · every later phase is built on these findings; a wrong one poisons them all.

### Phase 1 — Read the whole bid (the core value)

- **1.1** New fields from the bid PDF, each with page + quote: consignee rows (address, state,
  quantity, **delivery days**), estimated bid value, inspection required, ePBG duration (months),
  evaluation item-wise schedules, PAC items (fixed make/model), past-performance %, time for technical
  clarifications, "documents required from seller", links to spec / BOQ / buyer-ATC files.
  Check `sum(consignee qty) == total quantity` → else CONFLICTING. Files: `parsing/field_rules.py`
  (+ a small table reader if consignees need one), `tests/test_parsing.py`.
  → Sonnet · Medium · label rules against real fixtures; bump to High for money/quantity parsing (a 10× error is the worst bug).
- **1.2** Specification table per item ("Specification / Bid Requirement (Allowed Values)") as
  structured rows with page + quote.
  → Sonnet · Medium · table text from pypdf is messy; needs care, not design.
- **1.3** Download the files the bid PDF links to (buyer ATC file, spec PDF, BOQ detail), only those
  links, through `SafeFetcher`, size and page caps, stored by hash, at most 3 per bid, counted in the
  budget. PDF text only; scanned or non-PDF → "open it yourself" (OCR later, only if needed).
  Depends on 0.3 (are they public? the README's `probe` says buyer ATC files are).
  → Sonnet · Medium · security-relevant fetching (caps, link origin), but the guards already exist.
- **1.4** **Per-bid document checklist** from text ATC + attached files: each required document
  (turnover certificate, ISO/BIS, OEM authorisation, GSTR, toll-free number, service centre per state,
  financial document…) with page + quote, plus "≤10 MB and ≤100 pages per file; merge ATC certificates
  into one PDF". Deterministic patterns first (`parsing/clause_patterns.py`). Shown as a chat card.
  → Sonnet · Medium · extends existing pattern engine; the checklist wording matters to him.
- **1.5a** Design the LLM reading of ATC: JSON schema, prompt, quote check, what goes to Groq (public
  bid text only), cost cap, failure → "not read, check yourself". Write the prompt-injection test set first.
  → Opus · High · the highest-risk part of the system (untrusted text into a model).
- **1.5b** Build it: Groq call with no tools, schema-locked; drop any item whose quote isn't in the
  text; numbers re-read by code; injection tests pass before it is switched on.
  → Opus · High · security-sensitive; depends on 1.5a, re-verify the design before coding.
- **1.6** Corrigendum: keep the verbatim text; add an LLM summary under the same quote rule.
  → Sonnet · Medium · reuses 1.5b.

### Phase 2 — Know the seller well enough to check

- **2.1** Profile gets: states he can deliver to, certificates held, OEM or reseller (per product),
  "do you make this item yourself" (MSE EMD exemption), Udyam, DPIIT startup, years in business,
  ITR filed on GeM, PFMS-verified bank. Chat can propose them (still his Confirm). Onboarding warnings
  from video 2 (e.g. >24 months old and no ITR on GeM = can't bid). Files: `domain/models.py`,
  `infrastructure/database.py` (migration), `services/chat_tools.py`, `frontend/js/views/profile.js`.
  → Sonnet · Medium · plain model + migration + chat tool work.
- **2.2** Main products with key specs (only if D4 = yes).
  → Sonnet · Medium · small schema addition.

### Phase 3 — Checks (each one a new class in `eligibility/rules.py`)

- **3.0** Write down each rule's inputs, BLOCK vs REVIEW thresholds, and wording before coding.
  → Opus · High · decides when the app says "blocked"; a wrong block hides a winnable bid. Depends on 1.1 + 2.1 being right.
- **3.1** Delivery state: consignee states vs his states.
- **3.2** Certificates: asked (field + checklist) vs held.
- **3.3** OEM / authorisation / OEM turnover asked, and he is a reseller → review with quote.
- **3.4** EMD upgrade: none below ₹5 lakh; MSE exemption only if he makes the item; ATC limiting the
  exemption to the buyer's state.
- **3.5** Exact spec: bid's allowed values vs his product specs (only with 2.2).
- **3.6** Item-wise bids: which schedules he can bid on; total-value bids: he must quote every item.
- **3.7** PAC items: only the named make/model can bid.
- **3.8** Terms GeM forbids in ATC (GTC's list, e.g. experience only from one department, foreign
  certificates when an Indian standard exists) → "you may ask the buyer (representation)" with the
  last date from the representation rule (HANDOFF §4a).
  → 3.1–3.8: Sonnet · Medium · one small rule class + table-driven tests each, design fixed in 3.0.

### Phase 4 — Find bids better and earlier

- **4.1** GeM category names for his products from `mkp.gem.gov.in/search?q=` (public, shows the
  quadrant); he confirms; used as extra search words. Quadrant warning (Q1 OEM only, Q2 needs
  authorisation). Depends on 0.3.
  → Sonnet · Medium · one new public page type behind existing guards.
- **4.2** Listing filters he can use: bid type (BOQ / custom / service), end-date range; BOQ title
  words. Only through the page's own search, as today. Depends on 0.3.
  → Sonnet · Medium · touches the browser search, which must stay within the safety rules.
- **4.3** "New since last search" on bids and in chat.
  → Haiku · Low · a stored first-seen time already exists.
- **4.5** Import the bids GeM invites him to: he pastes the dashboard's "You are invited to participate in bid (GEM/…)" lines; the app finds each bid's PDF via the public listing search and checks it (live-tour.md).
  → Sonnet · Medium · bid number → PDF lookup through existing guards.
- **4.4** Scheduled search inside the running server (e.g. 9:00 and 15:00), respecting 15 min,
  5×2 pages, 250/day and the breaker; one at a time; skipped while stopped.
  → Sonnet · Medium · background timing in the server; must not double-run.

### Phase 5 — Tell him in time

- **5.0** Daily GeM check card: the app asks him each morning to look at *List of Bids → Already participated* and his dashboard and paste pending clarifications (bid, text, last date), orders pending acceptance, late deliveries, CRACs without payment, open SCNs. The app never logs in (live-tour.md: a buyer's shortfall request sat unnoticed there).
  → Sonnet · Medium · new form + table feeding 5.1.
- **5.1** In-app alerts list: new matching bids; closing in 3 days; representation window closing;
  "list your matching product 2+ days before the bid ends" (approval can take 48 h).
  → Sonnet · Medium · new table + chat card.
- **5.2** Outbound alerts per D3 (Mac notification first; email/WhatsApp only if chosen). Outbound only,
  never commands coming in.
  → Sonnet · Medium · small adapter; secrets kept in the data folder like the Groq key.
- **5.3** Export bids + verdicts + checklist as CSV (opens in Excel; no new library).
  → Haiku · Low · stdlib csv.

### Phase 6 — Past winning prices and competitors

- **6.1** For finished bids with his products: read the public result page (bidders, qualified or
  not, prices, L1), at most 10 a day. Depends on 0.3 (prices filled in?). `view_contracts` has a
  captcha: never.
  → Sonnet · Medium · new public page type behind existing guards.
- **6.2** Show past L1 prices for similar items on a bid and in chat; price range is advice only.
  → Sonnet · Medium · display + matching by item words.

### Phase 7 — Drafts he checks and sends himself (chat tools; the app never sends)

- **7.0** Prompt and wording rules for drafts (always marked "draft — check before sending").
  → Opus · High · drafts go to government buyers under his name.
- **7.1** Representation (pre-bid question) for flagged/forbidden clauses, with the last date.
- **7.2** Compliance sheet for custom bids (buyer's spec line → his offer → yes/no).
- **7.3** Make / Model / HSN list for BOQ bids (it goes onto the purchase order).
- **7.4** Rejection challenge text (he pastes the reason; 48 h window).
- **7.5** Listing pre-check (MRP −10%, 3 photos, MRP proof names this product, brand vs model).
- **7.6** Shortfall-reply helper: he pastes the buyer's clarification text; the app lists the documents asked, matches them to his profile and drafts the covering note. He uploads and submits himself.
  → 7.1–7.6: Sonnet · Medium · built on 1.x data and the 7.0 rules.

### Phase 8 — After he wins (needs the live tour first)

- **8.0** DONE 20 Oct 2026, see docs/live-tour.md (not opened: order-acceptance, ePBG and invoice-creation screens). Original text: Live read-only tour of his GeM account (he logs in himself, human speed, no
  submit/accept/pay/OTP clicks): orders, invoices, PRC/CRAC, payment, ePBG screen, incidents. Plan in
  `docs/live-tour-plan.md`, then he picks a date. Also finish HANDOFF §4a "Still not checked"
  (Payment Escalation SOP, current penalty policy, Revenue Policy v1.5, minimum delivery days, vendor check fee).
  → Opus · High · decides what the tracker must cover; a person's real account.
- **8.1** Order tracker: he pastes the contract PDF or types contract date, value, delivery days,
  ePBG %. The app works out every deadline from HANDOFF §4a (ePBG 15 days, delivery + LD per late
  week, buyer request 5 days, CRAC 10 days after proof of delivery, payment 10 days after CRAC,
  show-cause reply 10 days) and reminds him through 5.1/5.2.
  → Sonnet · Medium · date arithmetic from written rules; depends on 8.0.

### Phase 9 — Use it for real

- **9.1** Put the website online if D6 = yes; first check one real search from the server.
  → Sonnet · Medium · steps are in README; GeM may refuse data-centre addresses.
- **9.2** Two-week pilot with his father: fields he had to correct, bids it missed, time saved.
  → Opus · High · decides what to build next or whether to continue.

Order: 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9. Phase 0 steps that wait on D1/D2 don't block 1.1–1.4.

Housekeeping: videos and frames were **deleted on 20 Oct 2026** at the owner's request (~530 MB freed).
Only the 15 Hindi caption files remain in `../gem-videos/*.hi.vtt` (3 MB). To see a screen again,
re-download that one video at 480p (size check first). Frames were made with the bundled ffmpeg
(`uvx --with imageio-ffmpeg python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"`)
and `select='gt(scene,0.08)'`, keeping the last frame of each burst less than 3 s apart.

## Not verified yet

Chat never run against real Groq; website mode never deployed (HANDOFF.md §1).
