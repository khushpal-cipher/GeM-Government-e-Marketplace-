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
- The owner chose (20 Oct 2026): **plan first, then build everything**. The full build plan is in
  progress.md ("Build plan"), with phases 0–9, owner decisions D1–D7 and a model/effort note per step.

### Step 1: follow the build plan

Do progress.md "Next exact action", then the plan's steps in order, one at a time: failing test with a
saved fixture → make it pass → full suite → commit → update progress.md. Ask the owner only the
decisions D1–D7 (product, money, accounts); use the stated default when he hasn't answered.

### A. Build: see progress.md "Build plan" (replaces the old A list)

### B. Plan the live tour (no code; this is build step 8.0)

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
