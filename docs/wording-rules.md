# Wording rules (build step 1.0, 20 Oct 2026)

Everything the app drafts (shortfall replies, challenges, incident text, representations) or reminds
(alerts, the daily check card, the order tracker) follows these rules. Code:
`backend/src/gem_assistant/domain/wording.py` (`DRAFT_NOTE`, `deadline()`, `check_draft()`).
Every later step's tests run its drafts through `check_draft()` and its dates through `deadline()`.

## Drafts (text he sends to a buyer or to GeM)

1. **Starts with the draft note**: "DRAFT - check every line before you send it yourself on GeM. The app
   has not sent, uploaded or submitted anything." He removes it before sending.
2. **Never says the app acted**: no "submitted for you", "on your behalf", "the app sent", "uploaded
   automatically". The seller's own voice is fine ("We submit herewith the documents"): he is the sender.
3. **Never promises an outcome**: no "you are eligible", "you will win", "guaranteed", "100%".
   A bid is at best "no shortfall found"; NEEDS_REVIEW is never called eligible.
4. **Formal English** for anything to a buyer (government officers read it), even when he chats in
   Hinglish. Short: To / bid or contract number / Subject / 3-6 lines / his firm name.
5. **Only facts from his profile or the GeM text.** Anything the app doesn't know is a bracketed
   placeholder he fills: `[attach: OEM authorisation]`, `[your firm name]`. Never invented numbers.
6. **No PAN, bank account, IFSC, Aadhaar or phone** in a draft: GeM already has them, and drafts may be
   pasted into the chat (Groq).
7. Quotes the buyer's own words (clarification text, rejection reason) when replying, so the officer
   sees which point is answered.

## Reminders and deadlines (text the app shows him)

1. **Always a date, never only "within N days"**: "by Fri 23 Oct 2026, 5:00 PM (3 days left)".
   A date without a time means the end of that day. Always Indian time.
2. Past due says so plainly: "missed: was due Mon 19 Oct 2026 (1 day ago)", then what he can still do
   (e.g. raise a "delay in payment" incident).
3. Each reminder says **what**, **by when**, **where on GeM** (menu path, e.g. *Bids → List of Bids →
   Already participated*) and **what happens if missed** (e.g. "the order expires and invoicing is disabled").
4. A deadline from a rule not yet confirmed (HANDOFF §4a "Still not checked") adds
   "(GeM rule not confirmed; check on GeM)". If the app can't work a date out it says "date unknown",
   never a guess.
5. Language: the chat answers in his language (Hinglish in Latin letters if he writes Hinglish).
   Screen labels stay English, matching GeM's own menu names.
6. Tone: calm and short. No "URGENT!!!", no blame. The most urgent item comes first.
