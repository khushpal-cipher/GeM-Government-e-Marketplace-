# GeM training videos: what is on screen

What the 15 videos of the 2024 GeM training playlist (Rohit Semwal) **show on screen**: pages,
menus, buttons, fields, in order. Made by pulling a frame each time the screen changed and reading
it next to the Hindi auto-captions at the same time. Own words; nothing copied from the videos.

Playlist: https://youtube.com/playlist?list=PLffbgSv9050j2xxXP117UIAt3dkJszQBz (recorded early 2024).
Videos and frames are kept outside the repo in `../gem-videos/` (not committed).

How to read each section:
- **Time** is mm:ss in the video.
- **AI** is what our assistant may do on that screen (agreed in HANDOFF.md §2):
  **full** = can do it alone (public pages, reading, checking); **prepare** = can draft or fill in
  advice, the seller clicks; **never** = needs his login, an OTP, money or a legal promise.
- **Changed since 2024** is checked against HANDOFF.md §4a (official GeM rules, read 19 Oct 2026).
- The presenter's own PAN, bank and account numbers appear in some frames; they are left out here.

GeM site parts seen in the videos:

| Address | What it is |
|---|---|
| `gem.gov.in` | Public home page: search, Categories, Sign Up, Login, Bids, View Contracts |
| `mkp.gem.gov.in/registration/signup#!/seller` | Seller sign-up |
| `mkp.gem.gov.in/my-account#!/seller_profile/...` | Seller profile pages (one address per left-menu item) |
| `fulfilment.gem.gov.in/fulfilment/home` | Seller dashboard after login (orders, bids, catalogue, caution money) |

---

## Video 1: Introduction to the series (9:11)

Talking head only, no screens. He explains why he makes free GeM videos: sellers lack knowledge,
some get cheated by agents, and owners who pay someone else to run their GeM account should know
enough to check that person's work.

Nothing to record for the product.

---

## Video 2: Seller registration (22:08)

First 5 minutes: talking head (two kinds of GeM user, buyer = only government, seller = any
registered Indian business; one account can be reseller, OEM and service provider at once).

### Screens in order

| Time | Screen | What is on it | AI |
|---|---|---|---|
| 5:06 | `gem.gov.in` home | Top bar: Forward Auction, Bids, Sign Up, Login. Second bar: Categories, Features & Benefits, Business Opportunities, Sellers on GeM, View Contracts, CPPP, ODOP. Scrolling news line, "Ask GeMmy" chat button bottom-left | full (public) |
| 5:22 | Google search "gem registration" | Paid ads by private agents (sites that look like GeM). He warns: ignore anything marked sponsored, only use gem.gov.in | full |
| 5:40 | Home → **Sign Up** menu | Two choices: *Buyer Organisation* and *Seller/Service Provider* | — |
| 6:03 | **Seller/Service Provider Registration**, step 1 of 3: Pre-requisites | Steps bar: 1 Pre-requisites → 2 Terms & Conditions → 3 Registration. Says it must be done by an authorised person (director or proprietor). Dropdown *Business / Organisation Type*, PROCEED, "View pre-requisites document", link for weavers/artisans already registered with Ministry of Textiles | prepare (checklist) |
| 6:08 | Same, type = Proprietorship | A checklist appears. **Required:** Aadhaar (or personal PAN) with linked mobile; active email; business PAN (4th letter P or H for a proprietor); bank account + IFSC; ITR of last 3 years ("required for bid participation if business is older than 24 months"); registered address. **Optional** list below (Udyam/MSME etc.). He ticks all and proceeds | prepare |
| 6:42 | Step 2: Terms & Conditions | GTC PDF in a frame (the one shown is "GTC on GeM 4.0, Version 1.11, 21 June 2023"), tick "I have read and agree", PROCEED | never (legal promise) |
| 7:24 | Step 3: Registration, left menu: Organisation Details → Personal Verification → Email Verification → User Credentials | **Organisation Details:** type (locked), Business/Organisation Name, re-enter name (name can't be changed later), NEXT | never |
| 7:45 | Personal Verification | Radio: Aadhaar or Personal PAN; then number + linked mobile, OTP | never (OTP) |
| — | Email Verification, User Credentials | Not shown on screen; captions: email OTP, then choose a user ID and password | never |
| 8:43 | `fulfilment.gem.gov.in` dashboard (already-registered account) | "Hello <name>", star rating, "Know your Rank". Top menu: **Dashboard, Vivad se Vishwas, Market, Orders, Bids, Push Button Procurement, Catalogue**, user menu. Tabs: Notifications, Summary, Orders and Payments, Bid/RA, Category Insights, Product and Services, Incidents, GeM Stats, Reports. Boxes "Latest STC Updates" and "Latest Announcement" | never (login) |
| 8:46 | **Seller Profile** (`my-account#!/seller_profile/organisation_profile`) | Company name, GeM Seller ID, completion circle (100%), green line "You have completed your profile. You can now create catalogue, fulfil orders and participate in Bids". Left menu: **Business Profile** → Organisation Profile; *Mandatory:* Business PAN Validation, Business Details, Additional Details, Office Locations, Bank Accounts, Tax Assessment, e-Invoicing, MSME, Startup; *Optional:* Beneficial Ownership Compliance, Logistics, TAN Validation. Lower sections: Vendor Assessment, Seller Panel, Account Settings, User Management | never |
| 9:36 | Business PAN Validation | Picture showing where name/date/PAN sit on the card; fields: type, Business PAN, Name (as in PAN), Date (as in PAN); "Business PAN details verified successfully"; PROCEED | never |
| — | Business Details, Office Locations | Not shown on screen; captions: date of incorporation; "Add new office": address fields all mandatory, GSTIN optional | never |
| 10:35 | Bank Accounts | Tabs Manage / Add new Bank Account. Blue note: **PFMS verification is needed to get paid by buyers that pay through PFMS**; you can go on with a non-PFMS account and come back. Table: IFSC, bank name, account number, holder, PFMS code, "Is Primary?" switch | never |
| 11:11 | Tax Assessment | Note: if incorporated more than 24 months ago and no ITR added, **you can't take part in bids** and your turnover won't show. Note for proprietors exempt from ITR: verify GSTIN of registered office instead. Table: status (Verified), ITR type / PAN, assessment year, "Sale/Gross Receipts of business", EDIT; "Add New Tax Assessment" | never (data from his ITR); prepare (tell him which ITR figure to type) |
| 13:07 | e-Invoice Declaration | Explains IRP e-invoicing, mandatory above ₹5 crore turnover. Field *Turnover (max in 3 years)* with amount in words; radio "excluded from e-invoicing" Yes/No; long declaration tick box; GET OTP | never (OTP) |
| — | MSME | Not shown on screen; captions: Udyam number + **the same mobile as on the Udyam certificate** (common mistake) | never |
| 14:53 | Startup | Radio: Registered / Not registered with Startup India. Box lists DPIIT startup conditions (up to 10 years old, turnover never above ₹100 crore, innovation; a split-off business doesn't count) and says only DPIIT startups get exemptions from turnover, experience and EMD; link "Register now with Startup India" | full (explain) |
| 15:35 | Beneficial Ownership Compliance | Pink box: declaration under GFR Rule 144(xi) (bidder from a country sharing a land border with India), OM of 23 Feb 2023; if it applies, raise a helpdesk ticket with a compliance certificate. Radio "I certify that this seller is not from such a country"; SEND OTP, SAVE | never (legal + OTP) |
| 16:49 | Dashboard, pop-up | "Your TAN no. is not updated. Do you want to update now?" NO/YES (not needed for Vivad se Vishwas) | never |
| 17:32 | Dashboard → **Manage Caution Money Account** (`fulfilment/home#WORKSPACE_ID=CM_MANAGE_ACC_WS`) | Tabs Manage Account / Penalty and Refund. Box 1: a virtual account number, bank, IFSC (the account to pay into). Box 2: status Active, Threshold Limit ₹5000, Available Balance. Buttons: **Update Balance, Recalculate Threshold, Generate Challan and View Statement, Withdraw Excess Funds**. "Update Balance" → "Success: your Caution Money balance is updated" | never (money) |
| 20:21 | Talking head | Wrap-up: every new account starts as a reseller; OEM is next video | — |

Steps as he did them: gem.gov.in → Sign Up → Seller/Service Provider → pick business type → tick
document checklist → accept GTC → company name → Aadhaar/PAN OTP → email OTP → choose user ID and
password → log in → fill each red item in Seller Profile's left menu until 100% → (in 2024) pay
caution money → can now list products and bid.

### Changed since 2024

- **Caution money is gone** (waived for all sellers, discontinued 2025) [GTC cl. 27, SFAQ]. The
  Manage Caution Money page is now only for withdrawing old deposits ("Withdraw Excess Funds").
  So the step "pay caution money before you can do anything" no longer applies.
- The GTC shown at sign-up was v1.11 (June 2023); today's is v1.29 (25 Mar 2026).
- The rest of the flow (checklist, OTPs, profile left menu, 24-month ITR rule) matches §4a; not
  re-checked live.

### For the product

- The **profile left menu is a ready-made checklist**. Our profile chat could ask the same items
  (PAN type, years in business, ITR filed?, turnover max in 3 years, Udyam, DPIIT, land-border
  declaration) and warn early: "older than 24 months and no ITR on GeM = you can't bid".
- **PFMS-verified bank account**: some buyers pay only through PFMS. Worth a reminder in onboarding;
  not yet in HANDOFF.
- Everything here is **never** for the AI except explaining and checklists: it is all OTP, login and
  legal declarations.

---

## Video 3: Quadrants and how the product market works (21:33)

First 11 minutes: talking head explaining the four quadrants (already in HANDOFF.md §4). Then he
shows how to tell a category's quadrant on the site.

### Screens in order

| Time | Screen | What is on it | AI |
|---|---|---|---|
| 11:17 | Seller dashboard (`fulfilment.gem.gov.in`) | Same as video 2. He clicks **Market** | — |
| 11:26 | **Market** home (`mkp.gem.gov.in/market`) | Top: Dashboard, Market, Orders, Bids, Catalogue. **BROWSE** menu, category dropdown "All Categories" + search box. Banner and "POSHAN Abhiyaan Categories" tiles | full (public) |
| 11:56 | Category page **Ambulances – R** (`mkp.gem.gov.in/automobile-ambulances-r/search`) | Heading shows the name, then **"(Q1 Category)"**, then links *(Specifications)* and *(Sell in this category)*; "360° View" button. "Showing 1–12 products of 89", Sort by Price Low→High. **Left filters:** *Administrative* (Include Out Of Stock, Make in India, MSE, Startup, Seller Registered Address, Seller Rating, Lead Time For Dispatch), *Financial* (Annual Turnover), *Make/Model Selection* (Brand, Model), *Product Specifications*. Bottom bar: Product Compare, Product History | full (public) |
| 12:05 | Product cards | Each card: name, **Seller: OEM** or **Seller: Resellers**, rating band (e.g. 4.5–5.0★), **VA** badge (vendor-assessed OEM), sometimes a red **!** badge, Brand, *Min. Qty. Per Consignee*, offer price, MRP struck out, **% OFF**; small "startup" / MSE logos on some | full (public) |
| 12:41 | **Television (TV) (V2)** → "(Q2 Category)" | 856 products. Both OEM and Reseller cards. He explains **V2 = version 2** of the category (GeM rebuilt it), not quadrant 2 | full |
| 13:49 | **Executive Table (V2)** → "(Q3 Category)" | 13,503 products, mostly resellers; sorting High→Low shows OEM cards with VA badge | full |
| 15:10 | Product pages (three tabs open: ambulance Q1, TV Q2, table Q3) | Breadcrumb ends with the category and quadrant. Title, brand, model, price, **Trends** button. *Product Details*: Price For (1 piece/set), MRP/Unit, Offer Price/Unit, Availability (n in stock), Min. Qty per consignee, Product id, Country of Origin, **Local Content (MII) %**, Certification icon. *Seller Details*: Sold by OEM/Resellers, "OEM verified Reseller" ✓, "OEM verified catalogue" ✓, Seller Excellence rating, **VIEW ALL SELLERS**. Buttons **SELL THIS ITEM** (only on Q3/Q4 products, or Q2 once authorised) and **REPORT THIS PRODUCT**. *Specifications* list + VIEW MORE | full (public); "Sell this item" = never (his login) |
| 16:20 | My Account → Seller Panel → **Resellers Panel** (`admin-mkp.gem.gov.in/gem_users/company#!/reseller-requests`) | "Create New Reseller Request": Search Category (Products), four dropdowns Level 1→4 category (e.g. Domestic Appliances › Consumer electronics › Audio and visual equipment › Television (V2)); *Enter Authorization Details*: **Select Brand** (list of brands in that category) + **Authorization No** → **Request**. "Approved Requests" table below. With a made-up code: red bar **"Invalid Authorization Code"** | never (login); prepare (tell him which category path and brand to pick) |
| 18:05 | Ambulance page, **Make/Model Selection → Brand** list | Only real brands in Q1/Q2 (no "Unbranded") | full |
| 18:44 | Executive Table, Brand filter = **NA** | Shows "Unbranded Executive Table…", **Brand: NA**: the default unbranded option in Q3 | full |
| 19:10 | Same Ambulance page while **logged out** | Still shows "(Q1 Category)" next to the name: **the quadrant is public** | full |
| 19:21 | **Broom (V2)** → "(Q4 Category)" | 2,382 products; unbranded brooms from ₹10. Product page note: *"Local Content value is as declared by reseller since OEM is not registered on GeM"* | full |
| 19:53 | Talking head | Q5 and Q6 exist for innovative/startup products, but nothing is bought from them | — |

### Changed since 2024

- Nothing in §4a contradicts this video. Quadrant rules, V2 naming and the Resellers Panel are not
  covered by the official sources read so far; not re-checked live.

### For the product

- **The quadrant is printed next to the category name on the public category page**, e.g.
  "Ambulances – R (Q1 Category)". Our app can read it without login and tell him per product:
  "Q1: only OEMs, you can't sell this"; "Q2: you need the brand's authorisation number first";
  "Q3/Q4: you can copy an existing listing with Sell this item".
- Public category pages also give: number of products, sellers (OEM/reseller), price range,
  rating, VA badge, min qty, MII %. Useful later for price advice (always read-only, human speed).
- Category path has 4 levels (shown in the Resellers Panel dropdowns); handy for mapping his
  products to GeM category names (HANDOFF §2 "GeM category names").

---

## Video 4: Finding the right category; team logins; closing the account (16:23)

### Screens in order

| Time | Screen | What is on it | AI |
|---|---|---|---|
| 2:11 | Market home | Search box with category dropdown "All Categories" | full |
| 3:18 | Typing "sofa" | Suggestions list shows *keyword → category name* | full |
| 3:51 | **Category Results for "sofa"** (`mkp.gem.gov.in/search?q=sofa`) | Groups (Office Furniture, Office–Bamboo, Outdoor…) each listing categories **with the quadrant in brackets**, e.g. "Sofas (V2) (Q3)", "Sofa Set (Steel Tube) (Q3)". Red-ish warning: listing a product in a wrong or misleading category is prohibited, seller faces action under **GTC clause 3(A)(xiii)**, and contracts on such listings are void | full (public) |
| 4:03 | Category **Sofas (V2) (Q3 Category)** | "Search: sofa ×" chip; 9,596 products; cards as in video 3 | full |
| 4:58 | Product page breadcrumb | Home › Furniture and Furnishings › Commercial and industrial furniture › Office Furniture › **Sofa Set (Steel Tube) (Q3 Category)**: the full category path is on every product page | full |
| 5:27 | Searching "sanitizer" **inside** a category | "No products found for your search". Mistake: the dropdown was still set to that category | full |
| 6:35 | Search again with **All Categories** | "Category Results for 'sanitizer'": ~15 categories across Bath and Body, Computers, Cleaning…, quadrants Q2–Q4 | full |
| 7:29 | **BROWSE → Browse All Categories** (`mkp.gem.gov.in/browse_nodes/browse_list#!/categories`) | "Showing 1–10 of **11,960** categories"; search by category name; each row has **Specifications** and **View All Brands**; buttons *AR VR View Category*, **Download All Categories** | full (public) |
| 7:56 | Search "laptop" there | 9 categories (Laptop – Notebook, Rugged Notebook – Laptop (V2), Laptop Caddy…) | full |
| 8:24 | **Download All Categories** | PDF `all_category_name_desc.pdf`, "Product Categories (as on date 27-Jul-2023)", 502 pages, A–Z index | full |
| 8:59 | Catalogue → Services → **Search Offering** (`admin-mkp.gem.gov.in/admin/cat/service_catalogs#!/browse`) | Service categories as tiles (3D Printing Service, Advertisement Service – Magazine/Newspaper, AMC of fire extinguishers…), List/Grid, "All Categories" / "My Categories", search box. Typing "tuition" gives nothing = no such service category, so it can't be offered | prepare |
| 10:11 | Market → Services (`mkp.gem.gov.in/services#!/browse/`) | Same service tiles, each with a short description and SHOW DETAIL | full (public) |
| 10:51 | **BROWSE → Browse All Brands** (`.../browse_list#!/brands`) | "Showing 1–10 of **31,223** brands", A–Z letters, search; each brand → **View All Categories** (e.g. SAMSUNG: 42 categories) | full (public) |
| 12:35 | My Account → **User Management → Users** (`my-account#!/seller_profile/seller_users_list`) | "Primary user can create up to 50 secondary users". Tabs Manage Users / Add Secondary User. Table: Name, User Id, Roles, Email, Mobile, Status, Action; "ADD NEW SECONDARY USER". Captions: give an email and tick roles (bids, catalogue, order management); the person gets an invite link, verifies with Aadhaar and makes his own login | never |
| 14:55 | Account Settings → **Close Account** | Menu: Seller Profile, Update Aadhaar, Change Password, Change Email, Close Account. Closing is permanent and also closes secondary users. Blue box: "You have published catalogs, so you are not eligible to close seller account" (then GeM must close it on email request); check bank details before closing (for caution-money refund) | never |

### Changed since 2024

- Still 50 secondary users [SFAQ]. Category and brand counts will have changed (11,960 and 31,223
  in early 2024); the category PDF shown was dated 27 Jul 2023. Not re-checked live.

### For the product

- **`mkp.gem.gov.in/search?q=<word>` returns every matching category with its quadrant**, public.
  This is the cleanest way to turn his product words into GeM category names (HANDOFF §2), and to
  try synonyms automatically (the video's tip: phone / mobile / smartphone / cell).
- **Browse All Categories** + **Download All Categories** give the full category list; could be
  fetched once (read-only) instead of many searches.
- Warning worth repeating to him: listing in the wrong category is punishable and the contract is void.
- One login works in one place at a time; a second login throws the first person out and loses
  unsaved work. Tell him to give staff secondary users rather than sharing the password.

---

## Video 5: Listing a product by copying an existing one ("pairing / cloning") (20:34)

First 4 minutes: talking head. Two ways to list a product: copy an existing GeM listing
(pairing/cloning, ~5 minutes) or make a fresh one (video 6). Without a listing in a category, GeM
shows him no bids in it.

### Screens in order

| Time | Screen | What is on it | AI |
|---|---|---|---|
| 4:05 | Market → category **Chair Office (V2) (Q3 Category)** | 44,738 products. He filters **Brand = NA** (unbranded): 6,211 products | full (public) |
| 5:15 | Product page of an unbranded chair | Seller Details: **"Reseller not verified by OEM" ⚠** and **"Catalogue not verified by OEM" ⚠**; SELL THIS ITEM | full |
| 5:35 | Click **SELL THIS ITEM** → pop-up on `admin-mkp.gem.gov.in/#!/catalog/new?...gem_catalog_id=...` | "A gem catalog exists with this gem_catalog_id. Do you want to pair with it?" Ok / Cancel | never |
| 6:14 | Listing form, sections: **1 General Information, 2 Catalogue Information, 3 Offering Quantity & Price, 4 Product Specification, 5 Upload Images** | Section 3 opens. *Selling Product As* = Resellers (note: genuine OEMs claim OEM rights via the OEM panel; reseller details can't be edited after publishing) | never |
| 6:42 | Q3 product: **Authorization No.\*, Authorization Agency\*, Authorization Date\*, Authorization Validity From–To\*** | For a Q4 product (broom) these fields are absent. Captions: for unbranded/no-OEM products any details pass | prepare |
| 7:11 | **Country of Origin\*** (searchable list) | Note: origin applies to his offer only. Captions: **China is not in the list**. Picking India asks "declare local content as per Make in India?"; the paired listing's MII % is frozen. Fine print: if you disagree with the owner's MII %, don't pair; raise an incident instead | prepare |
| 9:33 | SKU, **HSN** number, **MRP in INR\*** (greyed, from the paired listing) + **Request MRP Change** link | Pop-up "MRP Change Request": Base price, Offer price, discount slabs, *MRP request documents* (e.g. Packaging Photo) + Upload | prepare (draft request + proof list) |
| 11:07 | **Offer Price Including Tax and Duties as INR\*** "(price for carted item will be locked for 10 days)" | Placeholder shows the **category price range "Range: [1500–38000]"**. Blue note: **"The price entered can't be increased for the next 30 days."** Typing 3500 on MRP 3599: tooltip **"Offer price needs to be at least 10% lower than MRP"**; 3000 accepted, shows 16.64% | prepare (suggest price) |
| 11:41 | **Discount** table | Quantity Start, Quantity End, Discount %, Price, +ADD SLAB | prepare |
| 12:26 | **Delivery Locations\*** | Red WARNING: refusing to ship a direct-purchase order to a location you selected is a **serious breach of GTC with grave consequences including permanent debarment**. Note: locations only apply to direct purchase orders | prepare |
| 12:33 | **State** grid by zone (North, Central, East, West, South, Northeast) with tick boxes per state | "Select states only if you can deliver to all districts and pin codes." Ticking a state adds all its districts/pins | prepare |
| 13:18 | **District** (search box) and **Pincode** | e.g. Mumbai, Pune only. Don't tick the state if you want only some districts | prepare |
| 14:04 | **Terms of Delivery** = "Free Delivery At Consignee Premises" (fixed); **Current stock / Maximum Quantity (to be delivered in 15 days)\***; **Minimum Quantity Per Consignee\***; **Lead Time for Direct Purchase\*** "Range [1–10]" days; tick "I have read and agree to the Undertaking" | Min qty hides him from buyers ordering less. Captions: buyers must give at least 15 days to deliver | prepare |
| 15:34 | Bottom: **REVIEW TERMS AND CONDITIONS**, tick "agreed… and the offering is matching GeM catalogue", **captcha**, PUBLISH | **SUCCESS!** "Product successfully uploaded… new catalogs may take **4–6 hours** to show on the marketplace and be available for bidding after approval (auto / GeM / OEM)" | never |
| 16:00 | Catalogue → Products → **Catalogue Search** (`admin-mkp.gem.gov.in/admin/cat/catalog/angular_catalog/#!/catalog/index`) | Note about OEMs under "GeM CMS 2.0". Tabs: **Inventory Notified, Discontinued, Notified Products, Published, Waiting For Admin Clearance, Waiting For Seller Clearance, More**. Table: Name, Title on Market Place, ProductID, Gem Catalogue id, Category, Brand, Model, MRP/NDP, Offer Price, Product Status, Inventory Status, Actions | never |
| 16:27 | Product page shows ₹1,500, not his ₹3,000 | Market shows the lowest price for the buyer's location | full |
| 16:45 | **VIEW ALL SELLERS** → **Other Sellers** (`.../all_sellers.html`), works **logged out** | Per seller: Offer Price, **Delivery Locations** (states/districts or All India), Quantity-based discount, Quantity Available, Min Qty/Consignee, Offer Product As, Country of Origin, OEM-verified flags, rating | full (public) |
| 17:06 | Branded products in Q3 (AARAV, Artifex) | Rule shown on the page: if both "reseller/catalogue **not** verified by OEM" → anyone may copy it; if verified → need that OEM's permission | full |
| 19:42 | Talking head | Next: fresh product upload | — |

### Changed since 2024

- **Minimum 10% below MRP** and **MRP change only 90 days after the last approved one**: still true [SFAQ].
- The success pop-up said 4–6 hours; GeM now says listings "normally" need **48 hours** to be
  approved [GTC cl. 4(e)]. The video's "up to 24 h to reach a bid" is out of date (see §4a).
- "Free delivery at consignee premises" matches [GTC cl. 6, 13].

### For the product

- **Other Sellers page (`.../all_sellers.html`) is public**: every seller's price, delivery area,
  stock, min qty and quantity discounts for one product. This is the data for price-range advice
  (HANDOFF §2 "AI can prepare: price-range advice"). Read-only, slow, few pages.
- Listing checklist the AI can **prepare** for him (he fills it in): category + quadrant, is the
  listing OEM-verified (can he copy it?), authorisation details if Q2, country of origin, HSN,
  offer price ≥10% under MRP and inside the category range, quantity slabs, states/districts he
  can **really** deliver to (warn: refusing a selected location = possible debarment), stock,
  min qty, lead time.
- Warn: the offer price can't be raised for 30 days.
