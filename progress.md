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

## Continue from here (written 20 Oct 2026)

The 15 videos are done; read the **summary at the end of `docs/gem-videos.md`** first.
Video progress: all 15 ticked:
- [x] 1  - [x] 2  - [x] 3  - [x] 4  - [x] 5  - [x] 6  - [x] 7  - [x] 8
- [x] 9  - [x] 10 - [x] 11 - [x] 12 - [x] 13 - [x] 14 - [x] 15

State: code unchanged since `ca5a4b1`; `cd backend && uv run pytest -q` → **398 passed** (20 Oct 2026).
The next session follows `docs/NEXT_SESSION_PROMPT.md` ("Full instructions").

**Next exact action:** ask the owner "build (A) or plan the live tour (B)?"; if he just says go, do A step 1
(list which extra bid-PDF fields are missing, then add them test-first).

Options:
1. **Live read-only tour** (Later #1 below). The videos never show orders, invoices, CRAC or
   payment, so the tour should cover only those, plus one check: is the buyer's **Red/Orange payment
   flag** visible anywhere without login (videos only show it on the logged-in bid page).
2. Or start building (HANDOFF §2 order). The videos sharpen steps 1–3:
   read the ATC page `fulfilment.gem.gov.in/contract/terms.jsp?bidra=…` + the buyer-uploaded ATC file
   + custom/BOQ spec PDFs; extract consignee address and delivery days, EMD amount, ePBG %/months,
   total vs item-wise, PAC items from the bid PDF; per-bid document checklist.
3. Past L1 prices: public result pages `bidplus.gem.gov.in/bidding/bid/getBidResultView/<id>`
   (found via all-bids with "Bid/RA Status"). `gem.gov.in/view_contracts` has a **captcha → never automate**.

Housekeeping: videos and frames were **deleted on 20 Oct 2026** at the owner's request (~530 MB freed).
Only the 15 Hindi caption files remain in `../gem-videos/*.hi.vtt` (3 MB). To see a screen again,
re-download that one video at 480p (size check first). Frames were made with the bundled ffmpeg
(`uvx --with imageio-ffmpeg python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"`)
and `select='gt(scene,0.08)'`, keeping the last frame of each burst less than 3 s apart.

## Later (in order)

1. Live read-only tour of the seller's own GeM account (he logs in; he agrees first). Cover only what
   the videos don't show: orders, invoices, receipt (CRAC), payment.
2. Leftover checks from HANDOFF.md §4a "Still not checked" (Payment Escalation SOP, current penalty
   policy version, Revenue Policy v1.5 PDF, minimum delivery days, vendor check fee). The 10 MB limit
   is now seen on screen in video 10 (2024; also max 100 pages per file).
3. Build in the order in HANDOFF.md §2: read the buyer's attached ATC file → early alerts for new bids →
   delivery-state / exact-spec / certificate / OEM checks + document checklist → past L1 prices.
   New ideas from §4a: show the buyer's Orange/Red payment flag; deadline reminders.

## Not verified yet

Chat never run against real Groq; website mode never deployed (HANDOFF.md §1).
