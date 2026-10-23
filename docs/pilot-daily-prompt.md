# Pilot daily check: prompt to paste (step 8.2, 23 Oct – 26 Oct 2026)

Runs as scheduled tasks: "gem-pilot-daily-check" on 24 and 25 Oct at 10:30, "gem-pilot-last-day" on 26 Oct at 2 PM (or paste the box below by hand).
Shortened to 4 days (23–26 Oct) by the owner on 23 Oct 2026.

```
You are running one day of the short pilot (build step 8.2, 23-26 Oct 2026) of GeM Assistant, a local app in
/Users/khushpalsinghchouhan/Documents/startup/GEM/GeM (branch docs/hinglish-testing-guide). Explain things in simple words.

STOP CONDITION: if today's date is after 26 Oct 2026, only say "The pilot ended on 26 Oct 2026." and stop.

RULES (from the owner, never break them):
- Read progress.md "Rules" first and obey them.
- Commit only on this computer. NEVER push, never open a PR.
- GeM in Chrome is the owner's father's seller account. Use the Claude in Chrome tools, in a NEW tab, read-only, human speed,
  other tabs untouched. Only open menus, tabs, filters and "view" windows, and close pop-ups with their × button. Never click
  submit, accept, upload, pay, download, "+ New", or YES/update on any pop-up.
  Never log in, never type an ID/password/OTP/captcha. If GeM shows the login page, stop the Chrome part, write "logged out"
  in the log and tell the owner to log in again.
  Never copy names, phone numbers, PAN, bank data or buyer designations into any file.
- Open bidplus pages ONLY through the "Bids → List of Bids" menu (a typed bidplus URL goes to the login page).
- Never reset the app's Safety page yourself. If fetching is stopped, write it in the log and tell the owner.

STEPS:
1. Read progress.md, docs/pilot-log.md (count the pilot day: day 1 was 23 Oct 2026) and "Pilot day 1" in docs/live-tour.md.
2. Make sure the app runs at http://127.0.0.1:8000 (curl /api/safety). If not, start the "gem-assistant" preview
   (.claude/launch.json).
3. curl http://127.0.0.1:8000/api/safety: note breaker open/closed and requests used today.
4. In Chrome: open https://fulfilment.gem.gov.in/fulfilment/home in a new tab. Read Dashboard → Notifications → "Latest Bids"
   (not in the accessibility tree: screenshot and zoom on the list). Write down the invited bid numbers (GEM/2026/B/…).
   Then Bids → List of Bids → filter "Bids/RAs Already Submitted/Participated": note any bid showing
   "Pending Clarifications" (bid number + last date only).
5. Give NEW invited numbers (not in the log yet) to the app, at most 5 per call, 15 minutes apart:
   first POST /api/bids/invited/parse {"text": "<the lines>"} to see which are already known, then
   POST /api/bids/invited/import {"bid_numbers": [...]}. A call can take minutes: run curl in the background and wait.
6. Start the app's daily search: POST /api/discovery/run; wait until GET /api/discovery says running=false;
   note outcome, found, new, downloaded, requests.
7. Compare: an invited bid that the keyword search (listings whose keyword is a profile category) did NOT find
   = "missed by the daily search". For each bid analysed today, check bid end date, EMD amount and total quantity
   against GeM's own bid card; note any mismatch, anything broken, wrong or confusing.
8. Append today's section to docs/pilot-log.md in the same format as earlier days. Facts only, with the date.
9. A clear, small bug: fix it with a test, run `cd backend && uv run pytest -q` (all must pass), commit locally.
   Bigger problems: only write them under "To build next".
10. Commit docs/pilot-log.md locally ("docs: pilot day N").
11. On the LAST day (26 Oct 2026) also write "Final report" in docs/pilot-log.md (bids missed, wrong fields, fixes made,
    what to build next or whether to continue), add a row for 8.2 to docs/done-log.md, update progress.md
    "Continue from here", commit locally, then remind the owner to fill the data-folder .env (GEM_SMTP_USER,
    GEM_SMTP_APP_PASSWORD = Gmail app password, optional GEM_SCHEDULE_TIMES="09:00,15:00", GEM_NOTIFY_TO) and to
    check / reset the app's Safety page if fetching is stopped.
12. Close the Chrome tab you opened. End with a 3-line summary in simple words.
```
