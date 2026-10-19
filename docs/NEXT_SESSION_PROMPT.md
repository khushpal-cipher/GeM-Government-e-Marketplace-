# Next session prompt

Updated 20 Oct 2026. Keep this file current: when the owner types
"give me a prompt", update progress.md and this file, commit locally, and reply with the box below.

## Prompt to paste

```
Continue GeM Assistant in ~/Documents/startup/GEM/GeM (branch docs/hinglish-testing-guide).

1. Read these fully before doing anything, in this order: progress.md, docs/NEXT_SESSION_PROMPT.md
   (follow its "Full instructions" exactly), docs/HANDOFF.md, docs/gem-videos.md (start with the
   summary at the end), README.md, ../docs/00-RESEARCH-AND-ARCHITECTURE.md. Then run
   `git log --oneline -10` and `git status`, and `cd backend && uv run pytest -q` (expect 398 passed).
2. Continue from progress.md "Continue from here". Don't redo anything under "Done".
3. Commit only on this computer. Never push, never open a PR: my friend is changing the GitHub repo.
4. Never log in to GeM, never solve or bypass a captcha, never submit anything on GeM. Public GeM
   pages only, read-only, within the app's existing safety limits.
5. Explain things to me in simple words. Ask me only about product decisions, money or accounts.
6. Keep progress.md accurate as you go (done / next exact action / not verified, with dates and
   commit hashes). Commit after every finished, tested step.
7. When I type "give me a prompt": update progress.md and docs/NEXT_SESSION_PROMPT.md, commit locally,
   and reply with the "Prompt to paste" box from that file.
```

## Full instructions

### Where things stand (20 Oct 2026)

- The 15 GeM training videos are fully written up in `docs/gem-videos.md` (screen by screen, what
  changed since 2024, AI level per screen, product summary at the end). Videos and frames were
  deleted on 20 Oct 2026 (owner's request); only the Hindi captions remain in `../gem-videos/*.hi.vtt`.
  To look at a screen again, re-download that one video (commands in git history of progress.md).
- Code is unchanged since the merge `ca5a4b1`. Tests: 398 passed on 20 Oct 2026.
- The owner has **not yet chosen** between building and the live tour.

### Step 1: ask one question

Ask the owner: "Start building (A) or plan the live read-only tour of your GeM account (B)?"
If he says "go" without choosing, do A.

### A. Build (HANDOFF §2 order, sharpened by docs/gem-videos.md)

Do one slice at a time; for each: write a failing test with a saved fixture, make it pass, run the
full suite, commit, update progress.md.

1. **More fields from the bid PDF** (the parser already reads ~26, see `backend/src/gem_assistant/parsing/`
   and HANDOFF §1). First list which of these are missing, then add them with page + quote evidence
   like the existing fields: consignee address(es) + quantity + **delivery days**; EMD amount; ePBG %
   and duration (months); evaluation method total-value vs item-wise (may exist); PAC items
   (fixed make/model); estimated bid value; inspection required; MSE/MII purchase preference;
   links to the specification document and BOQ detail document. Fixtures: use bid PDFs already in
   `backend/tests/fixtures/`; if a new one is needed, fetch one public bid PDF through the app's
   existing safe fetcher, never by hand-written scraping.
2. **Read the ATC**: the text ATC is at the end of the bid PDF ("Buyer Added Bid Specific Terms and
   Conditions") and, per the videos, on `fulfilment.gem.gov.in/contract/terms.jsp?bidra=…`; the
   buyer may also attach an ATC file. Check first whether these are reachable without login through
   the existing `UrlPolicy`/`SafeFetcher`; if a new host is needed, ask the owner before allowing it.
   Output: a per-bid **document checklist** (each required document, where it was asked, page + quote;
   remind ≤10 MB and ≤100 pages per upload, ATC certificates merged into one PDF).
3. Then early alerts for new bids, then delivery-state / exact-spec / certificate / OEM checks, then
   past L1 prices from public result pages (`bidplus.gem.gov.in/bidding/bid/getBidResultView/<id>`).
   `gem.gov.in/view_contracts` has a captcha: never automate it.

### B. Plan the live tour (no code)

Write `docs/live-tour-plan.md`: the owner logs in himself, human speed, read-only, no submit / accept /
pay / OTP clicks. Cover only what the videos don't show: orders (accept/decline, buyer requests),
invoices and GST invoice, PRC/CRAC, payment status, ePBG upload screen, incidents, and whether the
buyer's Red/Orange payment flag appears anywhere without login. For each screen: what to look at,
what to note, what AI level it would get. Then ask him for a date.

### Rules that don't change

- Commit locally only; never push or open a PR.
- No bot login, no captcha, no submitting on GeM (grave-penalty risk; decided 20 Oct 2026).
- Don't redo work listed under "Done" in progress.md.
- Simple words for the owner. Never copy personal data (PAN, bank, phone) from any GeM screen into the repo.
