# Recon findings (build step 0.3)

The **only** place GeM URL patterns, page shapes and field labels are written down (architecture doc
§ "Phase 0"). Code that relies on a GeM page cites a section here. Each fact has the date it was seen.

How it was done (22 Oct 2026): public pages only, logged out, every request through `SafeFetcher`
(4 s gap, contact email in the User-Agent) with the new `gem-assistant recon URL` command: URL rules
first, then the host's robots.txt, then the page once. Saved answers are in the data folder
(`<data folder>/recon/`, `<data folder>/corpus/20261022-0920/`), **not** in the repo: they hold seller
and officer names. GeM requests on 22 Oct 2026: 70 of 250 (corpus 52, probe 4, recon 14).

## 1. Hosts and robots.txt

| Host | robots.txt (22 Oct 2026) | Same as 13 Sep 2026? |
|---|---|---|
| bidplus.gem.gov.in | `Disallow: /resources/` and three `/bg_emd/epbgservice/...` paths | yes |
| mkp.gem.gov.in | comment line only (allows all) | yes |
| fulfilment.gem.gov.in | none (HTTP 404 = no rules) | first look |
| gem.gov.in, assets-bg | `/cgi-bin/`, `/resources/` (13 Sep; not re-read) | — |

`SafetySettings.blocked_path_prefixes` already refuses `/resources/`, `/cgi-bin/`, `/bg_emd/`.

## 2. Bid document PDF

`bidplus.gem.gov.in/showbidDocument/<doc_id>` (README). The listing's `b_id` **equals** the doc id
(22 Oct listing response). Text from pypdf comes in short lines: Hindi label, then English label,
then the value. A label can be split over lines: "Delivery Days" comes out as `/Delivery` + `Days`
(20 of 30 corpus bids have the consignee table; service, manpower and custom-service bids have none).
Consignee rows: officer name, `<6-digit PIN>,<address>`, quantity, delivery days.
30 corpus bids: all "Total value wise evaluation"; fixture `GEM-2026-B-7922876_doc9762022.pdf` is
"Item wise evaluation". Fixture picks for Phases 2-3: progress.md, "Continue from here".

## 3. Listing `/all-bids` and its filters

Seen in `tests/fixtures/all-bids-shell_2026-09-13.html` (13 Sep 2026). The listing search itself
worked live on 22 Oct 2026 (corpus run), but these filter keys were not re-compared with today's page. The page POSTs `payload={"page", "param", "filter"}` plus a CSRF token to
`/all-bids-data`. Keys (from the page's own `defaultLoad()`):

- `param.searchBid` (text), `param.searchType` = `"fullText"`
- `filter.bidStatusType`: `"ongoing_bids"` (default) or `"bidrastatus"` (finished ones)
- `filter.byType`: `all`, `product`, `service`, `bidToRA`, `custom`, `boq`, `rcbid`, `gt`, `lt`, `st`
  (labels: Product, Service, Bid To RAs, Product Custom, BOQ, Rate Contract, Global, Limited, Single Tender)
- `filter.byStatus` (only with `bidrastatus`): `tech_evaluated`, `fin_evaluated`, `bid_awarded`
- `filter.highBidValue`: `"highValue"` = estimated value >= Rs 2 crore, else `""`
- `filter.byEndDate.from` / `.to`: `yyyy-mm-dd`, both or neither, within +/-365 days
- `filter.sort`: `Bid-End-Date-Oldest` (default), `-Latest`, `Bid-Start-Date-Oldest`, `-Latest`

Listing fields that matter: `b_bid_type` (1 bid, 2 RA, 5 seen for reverse auction in tests),
`b_bid_to_ra`, `b_is_custom_item`, `ba_is_single_packet`, `b_eval_type` (>0 = schedule/item-wise),
`b_buyer_status` (>0 = results exist), `is_high_value`.
"Other details" per bid (representation info) is a **POST** `/public-bid-other-details/<b_id>`: not allowed.

## 4. Corrigendum

The listing page POSTs `/bidding/bid/viewCorrigendum/<doc_id>` (allowed prefix). Answer `0` = none,
else an HTML fragment. **First real ones captured 22 Oct 2026** (4 of 10 checked,
`corpus/20261022-0920/corrigenda/`), no phone or email inside. Shape, newest first:

    Corrigendum Details
    Modified On: 2026-10-19 15:31:42  Bid extended to 2026-10-22 10:00:00 (Auto Extension)
                                      Bid Opening Date: 2026-10-23 10:00:00 (Auto Extension)
    Modified On: 2026-10-16 15:30:12  Bid extended to 2026-10-19 10:00:00 (Auto Extension) ...

- "(Auto Extension)" = GeM extended it itself; without it the buyer did.
- A changed document comes as `Modified On: ... Download` with link
  `/bidding/bid/showcorrigendumpdf/<corrigendum_id>/<doc_id>` (not fetched yet).
- Both finished bids in §5 show a later end date than their PDFs (21-11-2025 vs 14-11-2025;
  19-10-2026 vs 12-10-2026): end dates move often, so the PDF's date alone is not enough.
Still shown verbatim only; parsing it for a new deadline is step 2.6.

## 5. Bid results (public, logged out)

The listing builds the "View Results" link (shown when `b_buyer_status > 0`):
`/bidding/bid/getBidResultViewSchedule/<b_id>` if `b_eval_type > 0`, else
`/bidding/bid/getSinglePacketResultView/<b_id>` (single packet) or `/bidding/bid/getBidResultView/<b_id>`.
RA results use `b_id_parent` and `/view-ra-schedules/<b_id>`.

Seen 22 Oct 2026, both HTTP 200, server-rendered HTML (no script needed for the tables):
- `getBidResultView/8506455` (GEM/2025/B/6819518, status "Cancelled"): **1. Bid details** (number,
  status, quantity, validity, start/end/opening, ministry/department/organisation; buyer name masked);
  **2. Technical evaluation**: per seller name, offered make/model/title, participated-on time,
  MSE/MII, **Qualified / Disqualified**; **3. Financial evaluation**: per qualified seller, total price
  and **rank (L1, L2...)**, with GeM's disclaimer "offered prices ... not approved / accepted prices".
- `getBidResultViewSchedule/9762022` (opened 20 Oct 2026, "Active"): bid details only; evaluation
  sections empty. So a result page "not opening" (live tour) can simply mean not evaluated yet.
  Here the buyer's name and email were **not** masked: never copy them.
- Disqualification reasons (`/bidding/buyer/getReason/<bp_id>`), seller evaluation
  (`/bidding/bid/viewSellerEvaluation/<bid_id>/<bp_id>`) and consignees
  (`/bidding/buyer/getConsignees/<bid_id>`) are **POST with a CSRF token**: not allowed (new POST
  paths need the owner's OK).
No Red/Orange buyer payment flag and no PBP notice on these pages.

## 6. Advance search `/advance-search` (public)

HTTP 200, 1.4 MB (the whole category list is in the page). Four tabs: bid details (bid/RA number,
category, end-date range), ministry/organisation/department, **consignee location** (state, city,
end-date range), **BOQ title** (end-date range). It POSTs `payload` + CSRF to `/search-bids`; the
lists come from POSTs `/state-list-adv`, `/city-list-adv`, `/ministry-list-adv`, `/org-list-adv`,
`/dept-list-adv`, `/boq-title-adv`. Payload keys: `bidNumber`, `category`, `bidEndFrom/To`,
`ministry`, `organization`, `department`, `bidvalue`, `state_name_con`, `city_name_con`,
`bidEndFromCon/ToCon`, `boqtitle_con`, `bidEndFromBoq/ToBoq`, `buyerState`, `searchType`, `page`.
None of these POST paths is allowed today. **`bidNumber` is an exact bid-number search**: a better
route for the 1.6 invited-bid lookup than the full-text listing (owner OK needed to allow
`/search-bids`).

## 7. Links inside a bid PDF (30 corpus bids)

| Link shape | Count | Public? |
|---|---|---|
| `mkp.gem.gov.in/uploaded_documents/.../OrderItem/BoqLineItemsDocument/...csv` | 96 | **yes**: CSV `Item Number, Item Title, Item Description, Item Quantity, Unit of Measure, Consignee ID, Delivery Period (In number of days)` |
| `mkp.gem.gov.in/uploaded_documents/.../OrderItem/BoqDocument/<date>/<name>[.pdf]` (spec, ATC, technical spec) | ~90 | not fetched; same host and folder as the CSV |
| `mkp.gem.gov.in/catalog_data/.../SpecificationDocument/...pdf` | 5 | **yes** (text PDF, spec table with "Compliance (Yes/No)") |
| `fulfilment.gem.gov.in/contract/slafds?fileDownloadPath=...` (buyer ATC file) | 23 | **yes**, but the one fetched is a **scanned image** (1 page, 2.4 MB, no text) |
| `bidplus.gem.gov.in/bidding/bid/bidsla/<n>` | 10 | **yes**: HTML, the standard Service Level Agreement text for that service category |
| `bidplus.gem.gov.in/resources/upload_nas/.../biddoc/...pdf`, `.../excel/...xlsx` | 35 | **never**: robots.txt `Disallow: /resources/` |
| `admin.gem.gov.in/apis/v1/gtc/pdfByDate/?date=YYYYMMDD` | 30 | GTC version in force on that date; not fetched |
| `bidplus.gem.gov.in/bidding/bid/showCatalogue/<token>`, `/bidding/downloadOmppdfile/`, `/bidding/bid/downloadMseMiiDoc/<id>/<n>.pdf` | 23/27/8 | not fetched |
| one non-GeM link (`vendor.powergrid.in`) | 1 | never (not a GeM host) |

The "text ATC page `contract/terms.jsp?bidra=`" from the plan **does not appear** in any of the 30 PDFs.

## 8. Marketplace search `mkp.gem.gov.in/search?q=` — NOT a captcha (22 Oct 2026, 11:50 pm, his Chrome, read-only)

Checked again by looking: normal page, results `li.bn-group > strong` (group) with `li.bn-link > a[href=/<category>/search#/?q=..]` and `<i>(Q2)</i>`; extra items are `more-bns hide`. The word "captcha" is only in its scripts. Fixture: `tests/fixtures/mkp-search-laptop_2026-10-22.html`. The older note below is kept for history.

(old) 22 Oct 2026, 09:45 IST:

22 Oct 2026, 09:45 IST: HTTP 200, but the page contains the word "captcha", so the classifier called it
a block and the **breaker tripped** (fetching stopped). Unknown whether it is a real challenge or
just a script on the page (blocked bodies are not saved). Category names/quadrant (4.1) and the
"Other Sellers" page (6.3) are therefore **not checked**. Next: the owner opens that URL in his
normal browser; if no captcha shows, he resets the breaker on the Safety page. Whatever it is,
`mkp.../search` must not be fetched again without a decision.

## 9. Not checked yet

- mkp search, category quadrant, a product's "Other Sellers" page (§8).
- Red/Orange buyer payment flag and PBP notices: not on the result pages; not found anywhere public.
- `BoqDocument` PDFs, `showcorrigendumpdf`, `showCatalogue`, GTC-by-date, MSE/MII documents.
- A finished **single packet** bid's `getSinglePacketResultView`, and an RA result.

## 10. What this changes in the build plan

- **2.1**: allow labels split over lines ("Delivery / Days"); services have no consignee table.
- **2.3**: fetch only `mkp.../uploaded_documents/` (CSV first: it gives item, quantity, consignee and
  delivery days cleanly), `catalog_data/...SpecificationDocument`, `fulfilment.../contract/slafds`
  and `bidplus.../bidsla/`. Never `/resources/`. Scanned ATC files → "open it yourself".
- **2.6**: real corrigendum fragments now exist (§4): "Bid extended to" + "(Auto Extension)" can be
  read by code, newest first.
- **2.7 / 4.6**: no public buyer flag or PBP notice found → 2.7 becomes "he notes it"; 4.6 dropped
  unless found later.
- **4.1, 6.3**: blocked on §8.
- **4.2**: bid type, finished status, high value and end date are plain `/all-bids` filters (no new
  path). Consignee state and BOQ title need `/search-bids` (new POST path: owner decision).
- **6.1**: result pages are public GETs with prices and L1 in the HTML: buildable now.
