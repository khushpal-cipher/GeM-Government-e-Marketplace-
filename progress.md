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

## Continue from here (written 22 Oct 2026)

State: `cd backend && uv run pytest -q` → **514 passed** (22 Oct 2026, after 2.1). Phases 0 and 1 and step 2.1 are done:
about 11 of 45 plan steps (~24%). D1 (Groq key) and D2 (contact email) are set. Build only in Claude Code.

**Next exact action:** step **2.2** (model now Sonnet, set 22 Oct 2026; Medium effort): specification table per item ("Specification / Bid
Requirement (Allowed Values)") as rows with page + quote. Real examples: corpus 9913333 (office tables),
10014519 (cartridges; the same table repeats on several pages). Read the text with
`PypdfTextExtractor` first; the table comes as label line, then value line(s). 2.1 left for later:
item-wise schedules ("Schedule N / item / quantity", fixture 7922876), PAC items (no real PAC bid in the
set yet: find one before coding), file links (2.3).

**Owner to do (safety stop, 22 Oct 2026 09:45):** fetching may still be **stopped**. He opened
`mkp.gem.gov.in/search?q=laptop` in his Chrome: it is a normal page (category names with Q2/Q3 tags, **no
captcha**), so the stop was a false alarm (the word "captcha" is in the page's code). He still has to press
reset on the app's **Safety** page (type "page looked normal, no captcha"). Check `container.safety.status()`
first; do not reset it for him. Steps 2.2-2.4 need no GeM requests, so building goes on meanwhile (2.3 fetches files: it needs fetching un-stopped).

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

Whether GeM's public listing search finds a bid by its bid number (1.6 lookup) is untested against real GeM: no contact email yet. Steps 1.3–1.5 were built by Gemini and reviewed only for test results and rule scans, not line by line.

Pasted-text parser (1.2) and shortfall helper (1.3) are tested only on invented text; no real GeM clarification was available.

Chat run against real Groq only for profile + refusal (20 Oct 2026); bid search and "what does bid N need" with a real bid not tried; website mode never deployed (HANDOFF.md §1).

Step 2.1 (22 Oct 2026): the new fields and consignee rows were checked against 34 real PDFs, but not by a person against the GeM screen. A consignee row split in an unusual way is left out and then shows as a CONFLICTING total, not as a wrong number. Past performance, ePBG months and inspection were seen in 12-27 of the 30 corpus bids; bids that lack a label simply show NOT_FOUND. Estimated value drops paise. The consignee table has no screen yet (API only). Bids stored before this step get their consignees only when re-read at start-up from the kept PDF.
