# Progress: GeM Assistant

Every session reads this file first and updates it before the session ends.
Details live in `docs/HANDOFF.md`; this file only says what is done, what is next, and where to continue.

## Rules (from the owner)

- Commit only on this computer. **Never push or open a PR**: a friend is changing the GitHub repo.
- Don't redo work listed under "Done".
- Explain things in simple words.
- **Update this file before the session ends**: move finished items to "Done", rewrite "Continue from here",
  add the date. Then commit it locally.

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
| 20 Oct 2026 | Decided: **no logging in or scraping GeM with a bot** (grave-penalty risk). A later live tour is read-only, the owner logs in himself, human speed, no submit/accept/pay clicks | — |

## Continue from here: watch all 15 videos ("Option A"), owner approved on 20 Oct 2026

Goal: learn what is **on screen** in every video (menus, buttons, fields, steps), not just what is said.

Playlist: https://youtube.com/playlist?list=PLffbgSv9050j2xxXP117UIAt3dkJszQBz (15 videos, ~4 h, 2024).

Steps:
1. **Check the download size first and tell the owner before downloading** (this was promised):
   `uvx yt-dlp -F <url>` or `uvx yt-dlp --print "%(title)s %(filesize_approx)s" -f "bv*[height<=480]+ba/b[height<=480]" <playlist url>`.
   Wait for his OK on the size.
2. Download at 480p into a folder **outside the repo**: `/Users/khushpalsinghchouhan/Documents/startup/GEM/gem-videos/`
   (never commit videos or frames). Also get the Hindi captions:
   `uvx yt-dlp --write-auto-subs --sub-langs hi --sub-format vtt ...`
3. ffmpeg is **not installed**. Either ask the owner to run `brew install ffmpeg`, or use the bundled
   binary: `uvx --with imageio-ffmpeg python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"`.
4. Save a frame each time the screen changes, e.g.
   `ffmpeg -i v.mp4 -vf "select='gt(scene,0.08)',showinfo" -vsync vfr frames/v02_%04d.jpg`
   (the showinfo log gives each frame's time). Drop near-identical frames. Expect ~300–600 in total.
5. Go video by video: look at the frames next to the captions at the same time.
6. Write `docs/gem-videos.md`, one section per video:
   steps in order (e.g. Dashboard → Catalogue → Add product), what each screen shows,
   timestamps, what changed since 2024 (check against HANDOFF.md §4a), and AI level per screen
   (full / prepare / never). Own words only; don't copy the videos.
7. Commit `docs/gem-videos.md` and this file after each few videos, so a cut-off session loses little.

Video progress (tick as done):
- [x] 1  - [x] 2  - [x] 3  - [x] 4  - [x] 5  - [x] 6  - [x] 7  - [x] 8
- [x] 9  - [x] 10 - [ ] 11 - [ ] 12 - [ ] 13 - [ ] 14 - [ ] 15

## Later (in order)

1. Live read-only tour of the seller's own GeM account (he logs in; he agrees first). Cover only what
   the videos don't show: orders, invoices, receipt (CRAC), payment.
2. Leftover checks from HANDOFF.md §4a "Still not checked" (Payment Escalation SOP, current penalty
   policy version, Revenue Policy v1.5 PDF, minimum delivery days, 10 MB limit, vendor check fee).
3. Build in the order in HANDOFF.md §2: read the buyer's attached ATC file → early alerts for new bids →
   delivery-state / exact-spec / certificate / OEM checks + document checklist → past L1 prices.
   New ideas from §4a: show the buyer's Orange/Red payment flag; deadline reminders.

## Not verified yet

Chat never run against real Groq; website mode never deployed (HANDOFF.md §1).
