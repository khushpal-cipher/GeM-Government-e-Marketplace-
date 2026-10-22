# Next session prompt

Updated 22 Oct 2026. The box below does not change from step to step: the next step lives in
progress.md. When the owner types "give me a prompt", update progress.md, commit locally, and reply with this box.

## Prompt to paste

```
Continue GeM Assistant in ~/Documents/startup/GEM/GeM (branch docs/hinglish-testing-guide).
Keep BUILDING from progress.md "Next exact action".

1. Read progress.md fully (short on purpose: rules, model table, next action, open notes). Then read ONLY
   what the next step needs: its entry in docs/build-plan.md (+ "How every step is built"), and the docs or
   recon sections progress.md names for it. Skim the code the step touches. Don't read other docs unless needed.
   Run `git log --oneline -5` and `git status`; run `cd backend && uv run pytest -q` once before committing.
2. One step at a time: failing test on a saved real fixture -> make it pass -> full suite -> commit the code
   -> ONE docs commit: a row in docs/done-log.md with that code commit's hash, and a new "Continue from here".
   Don't redo anything in docs/done-log.md.
3. Before each step, tell me in one line if I must switch model (table in progress.md); wait only for Opus steps.
4. Commit only on this computer. Never push, never open a PR.
5. Follow the Rules at the top of progress.md (GeM safety, my logged-in Chrome read-only, no personal data).
   Get what a step needs from GeM yourself; don't ask me to look or paste.
6. Ask me only about product decisions, money or accounts ("Decisions" in docs/build-plan.md; use the default
   if I haven't answered). Explain things to me in simple words.
```
