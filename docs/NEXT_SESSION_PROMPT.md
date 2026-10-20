# Next session prompt

Updated 20 Oct 2026 (final plan approved, building starts). Keep this file current: when the owner
types "give me a prompt", update progress.md and this file, commit locally, and reply with the box below.

## Prompt to paste

```
Continue GeM Assistant in ~/Documents/startup/GEM/GeM (branch docs/hinglish-testing-guide).
The FINAL build plan in progress.md is approved: start BUILDING now.

1. Read FULLY first, in this order: progress.md (the "Build plan" is the work list),
   docs/NEXT_SESSION_PROMPT.md (follow its "Full instructions"), docs/HANDOFF.md (§1 code gaps,
   §4a GeM rules = the deadline numbers), docs/live-tour.md. Read docs/gem-videos.md and
   README.md sections only when a step needs them. Skim the code the current step touches.
   Run `git log --oneline -5`, `git status`, `cd backend && uv run pytest -q` (expect 398 passed).
2. Do progress.md "Next exact action", then the plan's steps in order (0.1, then 1.0 to 1.6, then
   Phase 2...). One step at a time: failing test on a saved real fixture -> make it pass -> full suite
   -> commit locally -> update progress.md (Done row with commit hash, next exact action).
   Don't redo anything under "Done". BEFORE each step, tell me in one line if I must switch model
   (see "Which model to use" in progress.md), and wait for me if it's an Opus step.
3. Commit only on this computer. Never push, never open a PR: my friend is changing the GitHub repo.
4. The app and you never log in to GeM, never solve or bypass a captcha, never submit anything on
   GeM. Public GeM pages only, read-only, through SafeFetcher. If you need to see inside my account,
   ask me: I log in myself in my Chrome and you only look.
5. Ask me only about product decisions, money or accounts (D2-D7 in progress.md; use the default if
   I haven't answered). Explain things to me in simple words.
6. Keep progress.md accurate as you go (done / next exact action / not verified, dates, hashes).
7. When I type "give me a prompt": update progress.md and docs/NEXT_SESSION_PROMPT.md, commit locally,
   and reply with the "Prompt to paste" box from that file.
```

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
3. Before 0.2 / 0.3 / 1.6 lookup / Phases 4 and 6: ask the owner for D2 (contact email).

### Rules that don't change

- Commit locally only; never push or open a PR.
- No bot login, no captcha, no submitting on GeM (grave-penalty risk; decided 20 Oct 2026).
- Text he pastes from his GeM account stays on this computer; goes to Groq only when he asks the chat.
- Never copy personal data (PAN, bank, phone) from any GeM screen into the repo.
- Don't redo work listed under "Done" in progress.md. Simple words for the owner.
