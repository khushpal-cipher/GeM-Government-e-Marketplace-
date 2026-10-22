# Progress: GeM Assistant

Every session reads this file first (it is short on purpose) and updates it before the session ends.
Details live in `docs/HANDOFF.md`; this file only says what is done, what is next, and where to continue.

## Rules (from the owner)

- Commit only on this computer. **Never push or open a PR**: a friend is changing the GitHub repo.
- Don't redo work listed in `docs/done-log.md`.
- Explain things in simple words.
- **Anything a step needs from GeM (his account or a page): Claude fetches it from his logged-in Chrome** with the
  Claude in Chrome tools (owner, 22 Oct 2026). New tab, read-only, human speed, other tabs untouched; never click
  submit/accept/upload/pay/download/"+ New"; never log in, enter an OTP or solve a captcha (stop and tell him);
  never copy names, phones, PAN or bank data. Write what was seen, with the date, in `docs/live-tour.md` or
  `docs/02-RECON-FINDINGS.md`. Don't ask him to look, paste or click.
- **When EVERYTHING in the build plan is done, remind the owner about the `.env`** (owner, 23 Oct 2026): in the data folder's `.env` he must add `GEM_SMTP_USER=` and `GEM_SMTP_APP_PASSWORD=` (Gmail app password) for email alerts, and optionally `GEM_SCHEDULE_TIMES="09:00,15:00"` for the scheduled search and `GEM_NOTIFY_TO=`. Also remind him to reset the Safety page if fetching is stopped.
- **Build only in Claude Code** (owner, 22 Oct 2026). No Kimi / Gemini / other tools for now.
- **Update this file before the session ends**: add a row to `docs/done-log.md`, rewrite "Continue from here",
  add the date. Then commit it locally.
- When the owner types **"give me a prompt"**: update this file and `docs/NEXT_SESSION_PROMPT.md`,
  commit locally, and reply with the "Prompt to paste" box from that file.

## Which model to use (owner switches it in the app's model picker)

Default: **Sonnet · Medium**. Before starting each step, Claude tells the owner in one line if he must switch.

| Steps | Model · Effort |
|---|---|
| 0.3, 1.0, 2.5a, 2.5b, 3.0, 8.2 | **Switch to Opus · High**, switch back to Sonnet after the step |
| 2.1 | Sonnet · **High** (money and quantity parsing) |
| 0.1 | Sonnet · Low |
| 2.7, 4.3, 5.3 | Haiku · Low (or just stay on Sonnet) |
| everything else | Sonnet · Medium |

## Continue from here (written 23 Oct 2026)

State: `cd backend && uv run pytest -q` → **692 passed** (23 Oct 2026, after 7.1). Phases 0, 1, 3, 4 (4.6 dropped), 5 and steps 2.1-2.7 are
done: about 35 of 45 plan steps. Left: Phase 6 done;, Phase 7, Phase 8, plus 2.8/2.x leftovers listed below. D1 (Groq key) and D2 (contact email) are set; D4 = yes; D9 default: Phase 3 checks never block. Build only in Claude Code.

**Next exact action:** step 7.2 (compliance sheet for custom bids: buyer's spec line → his offer → yes/no; Sonnet · Medium). Read 7.2 in `docs/build-plan.md` and the spec-table code (2.2, `bid_spec`, 3.5) first. 7.1 done. Left from 7.1: forbidden-term flags only (no PAC / experience / turnover representations); no screen/chat card; GeM's Representation form length limit unknown. Left from 6.3: no screen/chat card; the public Other Sellers page has no locations (recon §8a); no category scan. Left from 6.2: no screen/chat card; per-piece wrong for multi-item bids; nothing fills the saved results yet (6.1 has no finder of finished bids). Left from 6.1: no finder of finished bids, no screen/chat card, `getReason` not built, not run on live GeM through the app, fixture rebuilt from seen text. Left from 5.3: not opened in real Excel; no filters.
Left from 4.7 (cities): only read bids are judged by city; Discover list is all-India; city spellings must be listed by him; search by city/state (4.2 Advance Search) not connected yet.
Left from 4.3: only the latest run counts as "new"; no New mark on the analysed-bids list.
Left from 4.2 rest: `advance_search` / `advance_lists` exist on `PlaywrightListingSource` but are not on any API route, screen or discovery run, and were never run on live GeM (first live run must save a real `/search-bids` answer as a fixture and check the real page works with our script stubs).
Left from 4.2: no "service" bid type, no screen for the filters.
Left from 4.1: `GET /api/categories?q=` only (no screen/chat card, no "he confirms", no saving extra words); a no-result page would count as a block (never seen).
Left from 3.8: the sample clause "within 07 days of receipt of supply order" (bid 9939006) is flagged as a forbidden term but is post-award: a false alarm to tighten
(exclude "supply order|receipt of|after award" in `forbidden_sample`).
Left from 3.5: tables are not tied to item numbers; no "not compared" list; he has not entered any products.
Left from 3.9: the chat cannot propose products yet; spec names are free text; he has not entered any products.
Left from 3.8: the patterns were never seen on a real forbidden term (none in the 30 bids); items 1, 3, 5, 6, 9, 12-14 not checked.
Left from 3.7: only one real PAC bid seen; other PAC wordings may be missed.
Left from 3.4: 9940677 still also shows "Couldn't find EMD required" (break right after "/EMD Detail"); `emd_state_limit` untested on a real sentence.
Left from 3.3: no real Q1 bid yet; Q tags are read from the whole item list, not per item.
Left from 3.2: standards inside the attached ATC file are not seen (2.4 checklist lists them); `ISI marked` is not a recognised standard.
Left from 3.1: the delivery-state result shows no city name; the check is not yet shown on any screen beyond the normal bid reasons list.
Left from 2.7: the buyer flag has no screen or chat card yet and no check uses it.
Left from 2.6: the corrigendum is summarised by the AI only when he asks (`read_terms`); a new deadline is not read by code into
DeadlineRule (the quote is only shown); changed-document corrigenda (`showcorrigendumpdf`) not fetched; not run on real Groq.
Left from 2.5b: no button on the bid page and the chat card ignores `ai_terms` (API + chat model only); AI clauses are not in
the bid's clause flags; Groq limits used are the documented base ones (8K tokens/min, 200K/day), not his key's limits page;
the AI may miss clauses (13 vs 23 items on the same text), so pattern flags always stay; a real sentence next to an injection
can still be listed as "Other clause to read".
Left from 2.4: text patterns on long ATC pages are high-recall (may over-list); attached-file results are cached per app run
only; not run against live GeM.

**Owner to do (safety stop, 22 Oct 2026 09:45):** fetching may still be **stopped**. He opened
`mkp.gem.gov.in/search?q=laptop` in his Chrome: it is a normal page (category names with Q2/Q3 tags, **no
captcha**), so the stop was a false alarm (the word "captcha" is in the page's code). He still has to press
reset on the app's **Safety** page (type "page looked normal, no captcha"). Check `container.safety.status()`
first; do not reset it for him. Building 2.4 needs no GeM requests; only running the attachment fetch for real needs fetching un-stopped.

**D8 answered 22 Oct 2026: YES to both POST searches** (not built yet): (1) Advance Search `/search-bids`
(exact bid number, delivery state, BOQ title), (2) `getReason` (why a seller was disqualified). Build later,
each as its own small step with tests, **never in the same step as 2.1**: allow the exact path in
`SafetySettings.post_allowed_paths/prefixes` (same SafeFetcher guards, no other POST path), then use (1) for
the 1.6 lookup instead of full-text search and for 4.2; use (2) in 6.1. They need the CSRF token the page
itself carries, so they go through the headless-browser page like `/all-bids-data`, not plain `get()`.
Not verified how that token is taken from `/advance-search` (recon §6): check before coding.

**mkp search page (recon §8) is NOT a captcha**: steps 4.1 (category names + quadrant from
`mkp.gem.gov.in/search?q=`) and 6.3 can proceed; the classifier must not call that page a block (the word
"captcha" appears in its scripts, so judge it by shape, like `Expect.HTML_FRAGMENT`). Fix that when 4.1 starts.

The owner's Chrome is logged in to GeM: Claude may LOOK there read-only (see rules below) if a step needs it.
2.1 does not.

Fixtures picked in step 0.2 (doc ids in `<data folder>/corpus/20261022-0920/pdf/`, bid no. in `manifest.json`):
- 9971825 simple product bid, 1 consignee, Delivery Days 15 (6 pages) - first test for 2.1
- 9913333 two-packet product bid, 4 consignees (12 p); 9941378 6 consignees; 9998303 9 consignees
- 9974983 and 9781965: 53 and 69 consignee rows (stress the quantity-sum check); 9974983 has 58 links
- 9885141 custom bid for services; 9748067 transport service (two-packet); 9995535 manpower (no inspection)
- 10009049 manpower, 26 pages. Missing from the set: item-wise evaluation, bid-to-RA (look for them in 2.1)

The owner's Chrome may be logged in to GeM (he logged in himself). Claude may LOOK there read-only if a
step needs his account (Claude in Chrome tools): open menus/tabs/"view" windows only; never click submit,
accept, upload, pay, "+ New" or anything that changes data; never copy names, phones, PAN or bank data.
0.2 and 0.3 use public pages only, through the app (SafeFetcher), not his logged-in browser.

## Where the rest is

- Finished steps (with commit hashes): `docs/done-log.md` (add a row after each step).
- The work list: `docs/build-plan.md`. Read only the step you build + "How every step is built" + "Decisions".
- GeM page facts: `docs/02-RECON-FINDINGS.md`. GeM rules: `docs/HANDOFF.md` §4a. Wording: `docs/wording-rules.md`. Live account tour: `docs/live-tour.md`.

## Not verified yet

Step 2.3 (22 Oct 2026): tested with a fake network, the real spec PDF (saved fixture) and a blank PDF standing in for the scanned ATC (the real one is 2.4 MB, kept out of the repo). Not run against live GeM through the app (fetching may still be stopped). robots.txt is not re-checked per file (it was checked for mkp and fulfilment in 0.2). Files are fetched but not yet stored against a bid or shown anywhere.

Whether GeM's public listing search finds a bid by its bid number (1.6 lookup) is untested against real GeM: no contact email yet. Steps 1.3–1.5 were built by Gemini and reviewed only for test results and rule scans, not line by line.

Pasted-text parser (1.2) and shortfall helper (1.3) are tested only on invented text; no real GeM clarification was available.

Chat run against real Groq only for profile + refusal (20 Oct 2026); bid search and "what does bid N need" with a real bid not tried; website mode never deployed (HANDOFF.md §1).

Step 2.2 (22 Oct 2026): spec rows were checked on 30 corpus PDFs by code (quote on page), not by a person against the GeM screen; a table whose columns sit at other x-positions than 24 / 162 / 366 would be misread (none seen). Bids stored earlier get spec rows only when re-read at start-up.

Step 2.1 (22 Oct 2026): the new fields and consignee rows were checked against 34 real PDFs, but not by a person against the GeM screen. A consignee row split in an unusual way is left out and then shows as a CONFLICTING total, not as a wrong number. Past performance, ePBG months and inspection were seen in 12-27 of the 30 corpus bids; bids that lack a label simply show NOT_FOUND. Estimated value drops paise. The consignee table has no screen yet (API only). Bids stored before this step get their consignees only when re-read at start-up from the kept PDF.
