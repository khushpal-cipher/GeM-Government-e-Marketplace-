# Live tour of the seller's GeM account (build step 8.0)

Done 20 Oct 2026, read-only. The owner logged in himself in his own Chrome (the built-in browser of the
Claude app blocks every file on `sso.gem.gov.in`, captcha included, so login is impossible there).
Claude only opened menus, tabs, filters and "view/details" windows. Nothing was submitted, accepted,
uploaded, downloaded or typed. No names, phone numbers, PAN or bank data are copied here.

## What each screen shows

| Screen (host) | What is on it | What it means for the app |
|---|---|---|
| Seller dashboard → Notifications (`fulfilment.gem.gov.in/fulfilment/home`) | "Latest Bids": **"You are invited to participate in bid (GEM/2026/B/…)"** (10 at a time) and "bid … extended to <date>"; Latest RAs; old announcements; PBP count | GeM itself sends him bid invitations. These numbers are a ready list of bids to check. He can paste them into the app (needs bid number → PDF lookup; import today needs a link) |
| Dashboard → Summary | Ratings (final 4.59, delivery, reliability, quality, buyer feedback); orders total / pending acceptance / pending delivery; bids total / won / lost; catalogue total / published / pending approval; transaction charges paid / pending; incidents | One-screen health view. The app can't read it (login), but he can tell the chat these numbers |
| Dashboard → Orders and Payments | Order value and count till date; counts by status (completed, cancelled, delivery in progress, paid, accepted, **pending acceptance**); monthly value trend; buyer-type and buying-mode charts | Status names for the order tracker (8.1) |
| Dashboard → Bid/RA | Participated / won / lost (count + value); lost by category; **"lost financial vs technical"**; last 10 lost bids | On this account half of the recent losses were **technical** (documents/eligibility). That is exactly what Phases 1–3 (read the whole bid, checklist, checks) prevent |
| Dashboard → Category Insights | Peer rating comparison; business by buyer type (here PSU 63 %, Centre 25 %, State 10 %) | Tells which buyers/keywords to search first |
| Dashboard → Product and Services | Sellers per category; catalogue status counts (e.g. discontinued); "Manage Products" | Listing work stays manual (videos 5–6) |
| Incidents (`incident.gem.gov.in`) | Counts: pending, escalated, SCN sent / responded / not responded, clarification sought, rectification, mutual resolution, closed, rejected. **"+ New" button: never click** | Show-cause (SCN) replies have a 10-day limit (HANDOFF §4a): the tracker should ask him about open SCNs |
| Orders (`…#WORKSPACE_ID=ORDERS_WS`) | 133 orders, 10 per page; per order: contract no, date, status, buyer designation, department, location, value, quantity; steps **Contract Placed → Consignment Dispatched → Consignment Received → Payment Completed**; links PAYMENT RECEIPT, AMC/TC E-INVOICE; filters (products/services, direct/bid/PBP, acceptance pending, in progress, completed, cancellation requested, payment completed…). A "GeM Sahay" loan pop-up opens first (close with ×) | The four steps are the tracker's stages |
| Order details (`…ORDER_SUMMARY`), tabs Product / Consignee / Shipment wise | Banner: **"raise invoice and deliver goods before the expiry date of the delivery period, else order will be marked as expired and invoice generation will be disabled"**; per consignee: quantity, dispatched, **expected delivery date**; per shipment: invoice no, dispatch date, amount, delivery date, icons Download Invoice / Dispatch Slip / e-way Bill / Details | Expected delivery date is the hard deadline; missing it blocks invoicing |
| Shipment "Details" window | GeM invoice no, delivery date, dispatch mode; **CRAC generated on <date>**; **Payment: "Payment not generated yet"**; dispatched / received / accepted / rejected quantity, rejection reason | Payment is due 10 days after CRAC (HANDOFF §4a). The tracker can say "payment late since <date>, escalate" |
| Bids → List of Bids (`bidplus.gem.gov.in/seller-bids`) | Filters: ongoing bids / ongoing RAs / **already participated**; bid type (product, service, bid-to-RA, custom, BOQ, rate contract, global); high value; status (technical / financial evaluated / awarded); end-date range. Per participated bid: status, **"Pending Clarifications: Click here to submit"**, "Clarification History: View", technical status (Qualified), bid/RA document, participation document, View Bid/RA Results, Check RA Eligibility | See next row |
| Clarification History window | Request no, time, type ("General clarification"), text (here: **shortfall documents** asked during technical evaluation: OEM turnover for 3 years, OEM authorisation), status Pending | **Most important finding.** A buyer's shortfall request sits silently on this page; missing it means technical rejection. Only visible after login |
| View Bid Results (`getBidResultView/<id>/participated`) | Bid details, buyer (name masked), technical and financial evaluation sections | The evaluation sections did not open on this bid (not checked why) |
| Bids → PBP Notices; Catalogue; RC offering; Vivad se Vishwas | Seen in the menu only, not opened | — |

## Changes to the build plan

1. **New step 5.0 "Daily GeM check" card** (in the app, no login by the app): every morning the app
   asks him to open *List of Bids → Already participated* and the dashboard, and to type or paste:
   pending clarifications (bid no + text + last date), orders pending acceptance, orders past expected
   delivery, CRACs without payment, open SCNs. These become alerts (5.1).
2. **New step 7.6 shortfall-reply helper**: he pastes the buyer's clarification text, the app lists
   the documents asked, matches them to the profile (2.1: certificates held, OEM or reseller) and
   drafts the covering note. He uploads and submits himself.
3. **New step 4.5 import invited bids**: he pastes "You are invited to participate in bid (GEM/…)"
   lines; the app finds each bid's PDF through the public listing search (existing guards) and checks it.
4. **8.0 is done** except: the order-acceptance screen (1 order pending acceptance today), the ePBG
   screen and the invoice-creation screen were not opened (they hold accept/submit buttons). Ask him
   to show them himself if needed.
5. **8.1 tracker stages and dates** are now fixed from the screens: Contract Placed → Dispatched
   (invoice before expected delivery date) → Received (CRAC date) → Payment (CRAC + 10 days).
