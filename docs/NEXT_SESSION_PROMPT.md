# Next session prompt

Updated 22 Oct 2026 (Phases 0 and 1 done; next 2.1). Keep this file current: when the owner
types "give me a prompt", update progress.md and this file, commit locally, and reply with the box below.

## Prompt to paste

```
Continue GeM Assistant in ~/Documents/startup/GEM/GeM (branch docs/hinglish-testing-guide).
Phases 0 and 1 are DONE (steps 0.1-0.3, 1.0-1.6). Keep BUILDING from progress.md "Next exact action" (step 2.1).

1. Read FULLY first, in this order: progress.md (the "Build plan" is the work list),
   docs/NEXT_SESSION_PROMPT.md ("Full instructions"), docs/HANDOFF.md (§1 code gaps, §4a GeM rules),
   docs/live-tour.md, docs/wording-rules.md. Read docs/gem-videos.md and README.md only when a step
   needs them. Skim the code the current step touches.
   Also read docs/02-RECON-FINDINGS.md (§2, §7, §10 for 2.1) and the "Continue from here" notes on D8 and the
   mkp page. Run `git log --oneline -5`, `git status`, `cd backend && uv run pytest -q` (expect 503 passed).
2. One step at a time: failing test on a saved real fixture -> make it pass -> full suite -> commit
   locally -> update progress.md (Done row with commit hash, next exact action). Don't redo "Done".
   BEFORE each step, tell me in one line if I must switch model ("Which model to use" in progress.md),
   and wait for me if it's an Opus step (2.5a is the next one; 2.1-2.4 are Sonnet).
3. Commit only on this computer. Never push, never open a PR: my friend is changing the GitHub repo.
4. The APP never logs in to GeM, never solves a captcha, never submits anything. Public pages go only
   through the app's SafeFetcher (contact email is set). I have no time to fetch things for you: **when a
   step needs something from my GeM account or a page, get it yourself from my Chrome** (Claude in Chrome
   tools; I am already logged in; open a new tab, don't touch my other tabs). Do not ask me to look, paste
   or click if you can look. Rules there: read-only, human speed, open pages/tabs/menus/"view" windows
   only; never click submit/accept/upload/pay/download/"+ New"/anything that changes data; never log in,
   enter OTP or solve a captcha (if GeM asks, stop and tell me); never copy names, phones, PAN, bank data
   into the repo or chat (write what the page contains in general terms, save only the page layout/labels).
   Write what you saw in docs/live-tour.md or docs/02-RECON-FINDINGS.md with the date.
5. Ask me only about product decisions, money or accounts (D3-D8 in progress.md; use the default if
   I haven't answered). Explain things to me in simple words.
6. Build only in Claude Code. Keep progress.md accurate (done / next / not verified, dates, hashes).
7. When I type "give me a prompt": update progress.md and this file, commit locally, and reply with
   this "Prompt to paste" box.
```

## For a different AI tool (not Claude)

Any coding agent can continue: it needs only this repo. Paste the box above. Model/effort advice in
progress.md ("Opus/Sonnet") means: use your strongest model for steps marked Opus (1.0 is done; 2.5a,
2.5b, 3.0, 0.3, 8.2 remain), a mid model for the rest. Code lives in `backend/` (Python, `uv run pytest -q`
must stay green: 451 tests on 20 Oct 2026) and `frontend/`. Same rules: commit locally only, never push,
never log in to GeM, never solve captchas, use `domain/wording.py` for every draft and deadline.

## Full instructions

### Where things stand (20 Oct 2026)

- Code unchanged since the merge `ca5a4b1`; 398 tests pass (20 Oct 2026).
- FINAL build plan written into progress.md (commit 356ce01) from the 15 videos and the live tour;
  the owner approved it and said start building (20 Oct 2026).
- D1 done: the Groq key is in `~/Library/Application Support/GeM Assistant/.env` (owner-only, outside
  the repo) and Groq accepted it. **D2 (contact email) is not set**: no `GEM_CONTACT_EMAIL` and no
  `contact-email.txt`, so nothing can reach GeM yet. Phase 1 needs no GeM requests.

### What to build first and why

1. **0.1** Chat against real Groq using `docs/testing-hinglish.md`; fix what breaks.
2. **Phase 1 (1.0–1.6)**, no GeM requests: wording rules (Opus), profile additions, daily GeM check
   card + alerts, shortfall-reply helper, order tracker + GeM charges, rejection reason + challenge
   draft, invited-bid import. Reason: the live tour found a buyer's shortfall request unanswered,
   an order pending acceptance and CRACs without payment; half his recent losses were technical.
3. D2 (contact email) is set; D8 (two extra read-only POST searches) was answered YES on 22 Oct 2026 but is not built.

### Rules that don't change

- Commit locally only; never push or open a PR.
- No bot login, no captcha, no submitting on GeM (grave-penalty risk; decided 20 Oct 2026).
- Text he pastes from his GeM account stays on this computer; goes to Groq only when he asks the chat.
- Never copy personal data (PAN, bank, phone) from any GeM screen into the repo.
- Don't redo work listed under "Done" in progress.md. Simple words for the owner.
