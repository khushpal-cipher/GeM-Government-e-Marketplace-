# Pilot log (step 8.2): 23 Oct – 5 Nov 2026

Claude runs the app once a day and checks it against his father's logged-in GeM account in Chrome (read-only).
The owner chose this instead of a pilot run by his father (23 Oct 2026). Daily prompt: `docs/pilot-daily-prompt.md`.
What the pilot measures: bids the app missed, fields it got wrong, things that broke. Time saved and "did an alert
help" can only be answered by his father (the owner says it saves time).

Ground truth for "missed": the bids GeM itself invites him to (Dashboard → Notifications → Latest Bids).

## Day 1: Thu 23 Oct 2026

| What | Result |
|---|---|
| GeM login in Chrome | Logged out twice ("expired or terminated due to multiple login"); the owner logged in again himself. GeM logs out quickly |
| Invited bids on GeM | 10: 8058451, 8190241, 8104270, 8180871, 8034651, 8188078, 8188061, 7965501, 8190647, 8190729 (all GEM/2026/B/…) |
| Invited bids read by the app (`/api/bids/invited/import`) | **10 of 10** (two batches of 5, 15 minutes apart) |
| Fields checked against GeM's bid card (end date, total quantity) | 19 of 20 bids match on both; 1 service bid (8152159, facility management) has no "total quantity" in its document, so the app shows none |
| Pending buyer clarifications (List of Bids → Already participated, first 5 of 118) | None seen |
| Profile keywords set for the pilot | toner cartridge, ink cartridge, copier paper, modular table, video conferencing (from the invites' "categories selected for notification"; the profile had only the test word "chair") |
| Daily search, GeM's default order | 100 bids found, **all closing the same day**; **0 of 10** invited bids found |
| Daily search, newest first (after fix) | 100 found, 88 new, closing 23 Oct – 13 Nov; **2 of 10** invited bids found (7965501 via "toner cartridge", 8190729 via "copier paper") |
| Safety | No stop; one GeM server error (HTTP 500) on one search; 69 of 250 requests used |

### Bugs found and fixed today (all tests pass: 704)

1. **Invited bids 6–10 were called "not on GeM".** The import takes 10 numbers but one search asks at most 5,
   so numbers 6–10 were never searched and then shown as NOT_FOUND. Now they say "ask again in 15 minutes". (6228c06)
2. **One GeM error threw away the whole search.** A server error on keyword 4 lost keywords 1–3. The search now
   hands back results one keyword at a time, so the ones before the error are kept. (6228c06)
3. **The Safety page said a server error stops all fetching.** It only ends that search; wording fixed. (6228c06)
4. **The daily search only saw bids closing today.** GeM sorts by "end date, oldest first" and the app reads 20
   per keyword, so every result closed that day. It now picks the page's own "Bid Start Date: Latest First". (14683b5)

### Seen but not fixed

- Bid 8034651: item category reads "Toner Cartridges / … (Q2) **3 3**" (two stray numbers from the next lines of the PDF).
- A facility-management service bid (8152159) was downloaded for the keyword "toner cartridge" (GeM's search matches loosely).
- Bids read before today keep the old listing rows; 5 bids analysed in the first run no longer have a listing row (list keeps 100).

### To build next (from day 1)

1. **Invites are the best bid finder.** GeM invites him across many categories (video conferencing, modular table,
   cartridges, copier paper, wooden shelf, double-sided tape, dough kneader, file/folder…). A keyword search with
   5 words finds only 2 of 10. Either read the invite list every day (he pastes it, or this daily check does) or
   allow more keywords than 5.
2. He bids far wider than his invites (lighting tower, split AC, installation and civil repair work in the
   "already participated" list): the profile needs his real product list, which only he or his father can give.
