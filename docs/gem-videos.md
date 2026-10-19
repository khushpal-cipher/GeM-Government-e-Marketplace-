# GeM training videos: what is on screen

What the 15 videos of the 2024 GeM training playlist (Rohit Semwal) **show on screen**: pages,
menus, buttons, fields, in order. Made by pulling a frame each time the screen changed and reading
it next to the Hindi auto-captions at the same time. Own words; nothing copied from the videos.

Playlist: https://youtube.com/playlist?list=PLffbgSv9050j2xxXP117UIAt3dkJszQBz (recorded early 2024).
Videos and frames were deleted after this write-up (20 Oct 2026); the Hindi captions are kept in
`../gem-videos/*.hi.vtt` outside the repo.

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

---

## Video 6: Uploading a new product (24:06)

First 3 minutes: talking head. Resellers can make new listings only in Q3/Q4 (Q1/Q2 are OEM-only).
Owning a brand (registered trademark) is different from being an OEM (which needs vendor
assessment); a reseller with a trademark can get the brand approved and list under it.

### Screens in order

| Time | Screen | What is on it | AI |
|---|---|---|---|
| 3:09 | Category **Executive Table (V2) (Q3)** → link **(Sell in this category)** | Opens `admin-mkp.gem.gov.in/#!/catalog/new?bnid=...` | — |
| 3:28 | Step bar with 5 dots: General Information → Catalogue Information → Offering Quantity & Price → Product Specification → Upload Images | Top: **"Find your Product Category in the Marketplace"** (search by keywords, or four Level 1–4 dropdowns) and **"My Categories"** (categories he already has products in, each with ADD ITEM). Link: "Cannot find a suitable category? Click here to submit a request for creation of a new category or to suggest changes" | prepare (pick category) |
| 3:50 | **1. General Information** | Category path line (Furniture and Furnishings >> Commercial and Industrial furniture >> Freestanding furniture >> Executive Table (V2)). Fields: Product Category, **Brand/OEM\*** dropdown (all brands in this category; "Unbranded" at the end), **"Couldn't find your brand? Click here to add"**, *Auto Create Catalogue*, **Clone Catalogue Specifications** (enter a catalogue id), **Golden Parameters\*** (GENERIC: frame, storage type, keyboard tray, footrest; MATERIAL: tabletop material…) | prepare |
| 4:55 | **"New Request"** pop-up (brand) | Request types: *We own a Registered Trademark for a Brand* / *We own a brand but have no registered trademark* / *We don't own a brand and want an OEM dashboard without a brand*. Brand name + Confirm. Note: **processing usually takes 7 days** by the GeM Brand Approval team; track it under Brand/OEM Requests. Captions: then website (or NA) + trademark certificate upload | prepare (gather documents); never (submit) |
| 6:21 | Catalogue → **Catalogue Search** → More → **Brand / OEM Requests** | "There are no products to show" (none filed) | never |
| 7:19 | Brand/OEM = **Unbranded**, then every golden parameter from dropdowns | Captions: values must be picked from the lists, **no free text**; if your exact spec isn't listed you can't type it | prepare (map his spec sheet to the dropdown values) |
| 9:04 | Pop-up after Save/Proceed | "Please find below existing products in the marketplace with the same specifications… you may pair… or click **Proceed with new item**". Here: "You have no matching product available, please upload new product matching buyer requirements to participate" | prepare |
| 10:23 | **2. Catalogue Information** | **Model\*** (50 chars), **Product Name\*** (100 chars), Product Description, Video url, Product Page Link (brand site page showing MRP), "Is there any active/current bid for this catalogue? Yes/No" | prepare (draft text) |
| 11:05 | **3. Offering Quantity & Price** | Authorization fields (as video 5); **Country of Origin**; "Declare local content as per **PPP-MII** policy?" Yes/No (can't change later); **Local Content %** (as per PPP-MII Order 29 May 2019; can't change for 30 days); **Make in India Declaration** tick (takes ownership; false % → action by GeM and buyers); SKU; HSN; **MRP in INR\*** | prepare (never tick the declaration for him) |
| 12:11 | **MRP Document Guidelines** + Upload MRP Documents\* | Document type list: Product Brochure, Government Order Copy, GST Invoice, Import Document, **MRP Declaration on OEM Letterhead**, Packaging Photo; "+ Add New Document". Captions: the proof must point clearly at this one product (not a 90-item brochure) | prepare |
| 14:02 | Offer price "Range [5000–150000]" (this category), discount slabs, delivery locations, stock, min qty, lead time, Undertaking tick | Same as video 5 | prepare |
| 15:10 | **4. Product Specification** | Long list of required dropdowns in groups (GENERIC, MATERIAL, EXTENDED RETURN UNIT, pedestal unit…), values quoting IS standards (e.g. "particle board grade II of IS 12823") | prepare |
| 15:49 | **Catalogue Document Guidelines** + Upload Documents\* | Accepted: OEM spec sheet/datasheet, **BIS certificate/licence**, OEM authorisation, GST invoice showing pack size/model, any mandatory licence (FSSAI, PESO, CE, USFDA, CPCB…). At least one needed | prepare |
| 16:07 | **5. Upload Images** | Three slots: Front view / Side-Top-Back view / Interior-close-up view. Guidelines: real product photo, **white background, no watermark or seller logo, ≤300 KB, jpg/png, 3 different angles**; tick "I certify that all images are distinct". Same file thrice → red bar **"Please upload distinct images"** | prepare (check photos) |
| 18:20 | Captions only | Model "Godrej" on an Unbranded listing, or "purple table" when the photo isn't purple → rejected. Photo, name and specs must agree | full (check) |
| 18:40 | Review T&C, tick, captcha, PUBLISH | **SUCCESS!** "queued for review… see it under **Waiting for Admin Clearance**" | never |
| 19:10 | Catalogue Search → **Waiting For Admin Clearance** tab | His listing with status "Waiting for Admin Clearance"; another row shows **"Awaiting OEM Approval"** | never |
| 19:56 | **Notified Products** tab | Rejected listing: Product Status "Incomplete", Inventory "Stock Expired", links **Admin Rejection reason**, Show Reasons, edit; red "Stock Note: the stock has been marked invalid". Pop-up lists Field + Reason, e.g. *Make → "kindly mention the brand name"*; *ISI CM/L number → "if ISI marked is yes, must specify CM/L no."*. Fix with edit and resend | prepare (read reasons, draft fixes) |
| 20:41 | **Session Expiration Warning** | "Because you have been inactive, your session is about to expire" STAY LOGGED IN / LOG OUT NOW | — |
| 21:27 | A published listing's page | Captions: **published listings can't be edited**; to change a spec, make a new listing | full |
| 22:12 | **Clone Catalogue Specifications**: paste the old product's catalogue id → Submit | All golden parameters fill in automatically; only price, MRP proof etc. left | prepare |
| 22:55 | Talking head | Next: services | — |

### Changed since 2024

- Success pop-up says 4–6 hours; GeM now says listings normally need **48 hours** [GTC cl. 4(e)].
- MRP change only 90 days after the last approved MRP [SFAQ]; not shown here.
- Brand approval "usually 7 days" is from the 2024 screen; not re-checked.

### For the product

- Biggest prepare-only job here: **turn his product spec sheet into GeM's dropdown values** for a
  category, and list the missing ones before he starts (no free text is allowed).
- **Pre-check before he publishes**: brand vs model text, photo vs colour/spec, 3 distinct
  white-background photos ≤300 KB, MRP proof that names this exact product, at least one
  catalogue document (BIS etc.), offer ≥10% under MRP and inside the category range.
- **Read rejection reasons** from Notified Products (he pastes them) and suggest exact fixes.
- MII %: tell him it is locked once declared and false values are punished.

---

## Video 7: Becoming an OEM (vendor assessment) (20:11)

First 10 minutes: talking head (already in HANDOFF §4: everyone starts as reseller; RITES does a
document check then a video check; exemptions; trademark vs no trademark).

### Screens in order

| Time | Screen | What is on it | AI |
|---|---|---|---|
| 9:55 | My Account → **Vendor Assessment → Assessments** (`my-account#!/seller_profile/vendor_assessments`) | Rules box: vendor assessment is **mandatory for OEMs** unless exempt; checks capacity and past performance; a **non-refundable fee** is paid online to the verifying agency; assessment is **finished within 15 days of payment**; seller can object **within 5 days** of the draft report. Table: Seller Name, Status, Assessor Status, Created At, Marked for Revert At, Actions; **NEW ASSESSMENT REQUEST**. Sub-menu: Assessments, Assessment Exemption Documents, Assessment Exemption | full (explain) |
| 10:35 | **Vendor Assessment** wizard (`mkp.gem.gov.in/vendor_assessment#!/index`) | Left steps: **Assess me As → Vendor Profile → Bank Account Details → Category details → Financial details → Submit VA** (and Assessor Response later). "Assess me as": Manufacturers or OEMs / Resellers | never |
| 10:58 | Vendor Profile | Profile values copied from his account; asks **Additional Contact Number\*** and **Additional Email ID\*** | never |
| 11:07 | Bank Account Details | Fetched from profile; PROCEED | never |
| 11:32 | **Category Details** | "Category for which vendor assessment required": Offering type (Product), Category\* (type-ahead, e.g. "table" → Executive Table (V2), Table Mats…), Description\*, **Production Capacity per month\***, OEM authorization tick; ADD NEW ROW (no limit). **Sold Details**: Sold to type, Entity/Govt ministry, Year, Category, Quantity, Sold Value (₹) | prepare (list his made-in-house categories, capacity, past sales) |
| 13:22 | Financial details | His ITR rows (ack number, year, turnover, P&L, ITR type) fetched from profile | never |
| 14:26 | **Submit VA** | "Vendor Assessment details are completed. Proceed to submit." → **Submission success!!!** with a VA id and time. Captions: a login for the agency's site comes by email; documents there, then fee, then video assessment, then report | never |
| 14:53 | **Assessment Exemption** (`.../vendor_assessment_exemption`) | Box: sellers with **₹500 crore+ turnover, BIS licence holders for that category, central/state PSUs, govt departments** are exempt; **exemption check is free**; agency takes **2 working days**. NEW EXEMPTION REQUEST | full (tell him if he may qualify) |
| 15:41 | Exemption wizard → **Assessment Exemption Criteria** | Options: Central/State PSUs; **OEMs holding BIS licence for that product category**; sellers recommended by a CPSE/govt department for set categories and period; registered societies/trusts with government representation; vaccine makers on the Health Ministry list; drug makers with notarised undertaking + valid drug licence; medical-device makers with a valid manufacturing licence. Then Category details → Documents → Submit | prepare |
| 16:38 | Talking head | Trademark: with a registered trademark his listings are approved instantly; without one he can still be an OEM as "BrandName – CompanyName" (affidavit) or "Unbranded – CompanyName", but each listing waits for GeM checking | — |

### Changed since 2024

- Vendor-assessed sellers are **exempt from EMD** [GTC cl. 4(m)], a strong reason for a maker to do it.
- Exemption list matches §4 of HANDOFF. **Fee amount still not checked** (listed in §4a "Still not checked").

### For the product

- Simple yes/no check from his profile: "Do you make this item yourself? Do you have a BIS licence
  for it? Turnover ≥ ₹500 cr?" → suggest exemption request (free, 2 days) or paid assessment.
- Tell makers the payoff: OEM panel → can list in Q1/Q2, authorise resellers, and no EMD.

---

## Video 8: Listing a service (11:25)

First 4 minutes: talking head. GeM has products and services only (no "job work"). A product's
own after-sales service can't be listed as a service; only GeM's standard service categories
(manpower, security, catering, vehicle hiring, horticulture…). No category = can't list (e.g. tuition).

### Screens in order

| Time | Screen | What is on it | AI |
|---|---|---|---|
| 3:52 | Catalogue → Services → **Add new offering** (`admin-mkp.gem.gov.in/admin/cat/service_catalogs#!/browse/`) | Service tiles (3D Printing, Advertisement, Afforestation, Air Ambulance, AMC/CMC of Fire Fighting Equipment, AMC of Integrated Security…), List/Grid, **All Categories / My Categories**, search "Search Service Name/ID" | prepare |
| 5:11 | Search "air conditioner" | Suggestions: Annual Maintenance service Air Conditioner; Comprehensive Annual Maintenance Services for Precision Air Conditioners; Hiring of Air Conditioners and Desert Coolers (event / monthly) | full |
| 5:32 | Service page (e.g. *Comprehensive Annual Maintenance Services for Precision Air Conditioners*) | **Description** (what the service is; buyers/sellers with problems mail services.gem@gem.gov.in with subject "Organisation \| Service Category"), **Service Level Agreement** (expandable), green **Create** | full (read SLA) |
| 5:53 | After Create | Green bar "Service Catalogue initiated, fill details and click VALIDATE & SAVE…". Sections: Description, SLA, **Experience**, **Rate Sheet**, (Certificates for some) | never |
| 6:31 | **Experience** | "Relevant project experience of same and similar service in the last 3 years (max 3) from any Central/State Govt org / PSU / Public Listed Company". Project 1: Organisation Name\*, Order Number\*, Current Project Status (Completed), Project value (₹)\*, Date of commencement / completion, **Upload Relevant Document\***; "+ Add New Project". Captions: new sellers can skip it | prepare (collect his POs / completion certificates) |
| 6:56 | **Rate Sheet** | Table of dropdown columns for this service (e.g. Type of precision AC system, Capacity, Vintage, Dedicated manpower at site, Condition of equipment, Type of AMC, Type of CAMC provider); Edit, Add row | prepare |
| 7:14 | **Validate & Save** | "Service Catalogue Saved"; green line **"This Service Catalogue has been approved and is live"**; red **Deactivate the Offering** button | never |
| 7:43 | **Security Manpower Service (Version 2.0)** → Create | Extra section **Certificates**: **PSARA certificate — mandatory**; "User Manual for Service Provider" link; "Refer to this link for Service Approval Process/SOP" | prepare |
| 8:20 | A manpower service → Certificates | ISO certificate (optional), Compliance with Labour Laws (optional), **Undertaking for Labour Identification Number (LIN) — mandatory** | prepare |
| 9:03 | Talking head | Catalogue part done. Next: how orders come (bids, or direct purchase) | — |

### Changed since 2024

- Nothing here conflicts with §4a. Service listings going live at once (unless a certificate is
  mandatory) not re-checked.

### For the product

- For a service seller, the AI can check before he starts: does the category exist, which
  certificates are **mandatory** for it (PSARA, labour/LIN, food licence…), and whether he has up to
  3 government/PSU/listed-company projects from the last 3 years with documents.
- The service's SLA text is readable; the AI can summarise it (penalties, response times) for him.

---

## Video 9: Bid types and how to search bids (23:57)

Two ways to get orders: bids (GeM sends him bids in categories he has listed) or direct purchase.
Most of the bid-type explanation (4:36–18:23) is spoken over the bid list page; summary is in
HANDOFF §4 (product, service, bid-to-RA, custom ≥21 days, BOQ ≥5 items, bunch, PAC).

### Screens in order

| Time | Screen | What is on it | AI |
|---|---|---|---|
| 3:55 | `gem.gov.in` home, logged out | Banners: **Vivad se Vishwas – I** (relief for MSEs: refund of forfeited PBG, EMD, LD, risk purchase; revocation of bans), ODOP; news line about IPIndia outage delaying brand/OEM approvals (Mar 2024) | full |
| 4:14 | **Bid Listing** (`bidplus.gem.gov.in/all-bids`) | Note "It may take up to **15 mins** for newly published or modified bids to show". Keyword box with "Contains" option. **Filters:** Ongoing Bids/RA, Bid/RA Status; *By Bid Type*: All, Product Bid/RAs, Service Bid/RAs, **Bid To RAs**, **Product Custom Bid/RAs**, **BOQ Bids**; *By Bid Value*: **High Value Bids**; Bid End Date From/To. Sort "Bid End Date: Oldest First". ~39,685 records | full (public; our app already reads this page) |
| 4:33 | One bid card | Bid No. (e.g. GEM/2024/B/…) → **RA NO.** (if bid-to-RA), Items, Quantity, Department Name and Address (ministry / department), Start Date, End Date, **View Corrigendum/Representation**, **View RA Schedules** | full |
| 18:23 | Search by bid number → click the blue bid number | Bid PDF downloads (`GeM-Bidding-<n>.pdf`, 7 pages here). First-page table (Hindi + English): Item Category, Contract Period, **Minimum Average Annual Turnover (3 yrs)**, **Years of Past Experience**, **MSE exemption** for experience/turnover, **Startup exemption**, **Documents required from seller** (with note: if claiming exemption, upload proof), **Bid to RA enabled**, **RA Qualification Rule** ("50% lowest priced technically qualified bidders"); page 2 "Bid Details": Type of Bid (e.g. Two Packet Bid) | full (our app already parses this) |
| 19:05 | Keyword "air conditioner" | 2,418 matching bids (any bid whose items contain the words) | full |
| 19:30 | **Advance Search** (`bidplus.gem.gov.in/advance-search`), only when **logged out** | Tabs: **Search by Bid/RA Details** (bid number, **Category** dropdown, end date range), **Search by Ministry/Organization** (Ministry\*, State\*, Organisation, Department, dates), **Search by Consignee Location** (Consignee State\*, Consignee City, dates), **Search by BOQ Title** (BOQ Title\*, Bid Value, dates). Note "This search is available for Ongoing Bids only". e.g. Television Tv, 21–31 Mar → "No data found"; Laptop – Notebook → list | full (public) |
| 21:16 | Consignee location result | Shows all categories for that city; you **can't combine city + category** | full |
| 21:56 | BOQ Title search | Buyers can now give BOQ bids a title, so you can see what a BOQ is about without downloading | full |
| 23:56 | Talking head | Next: taking part in a product bid | — |

### Changed since 2024

- Bid-to-RA "50% lowest priced technically qualified bidders" still true [BFAQ].
- Captions say custom and BOQ bids run **at least 21 days** and normal bids 10 days; not in §4a sources; not re-checked.
- Vivad se Vishwas–I was a 2023–24 scheme; whether still open not checked (not product-critical).

### For the product

- The app already reads `bidplus.gem.gov.in/all-bids` and the bid PDF. The screens show **filters it
  doesn't use yet**: bid type (product / service / bid-to-RA / custom / BOQ), High Value, end-date
  range, and the Advance Search by **category**, **ministry/state**, **consignee state/city** and
  **BOQ title** (HANDOFF §2 "GeM filters"). Advance Search only works logged out, which suits us.
- New bids can take 15 minutes to appear: alerts can't be faster than that.
- Custom and BOQ bids have no category, so a category-based search misses them; search them by
  keyword / BOQ title too.

---

## Video 10: Taking part in a product bid (33:28)

The core video. He walks through four real bids (broom Q4, broom V2 Q4, lyophilizer Q3, e-cart garbage Q3).

### Screens in order

| Time | Screen | What is on it | AI |
|---|---|---|---|
| 2:25 | Dashboard → **Bids** → `bidplus.gem.gov.in/seller-bids` (logged in) | Same filters as the public list plus **Participated Bids** and **By Category: "None selected"** (only categories he has listings in). Pink box: you must pick a category first; the search box finds nothing without one; to see all bids, log out and use `bidplus.gem.gov.in/all-bids`; use "Exact Bid Search" if you know the number | never (login) |
| 3:32 | Category = Broom Sticks… | Bid cards now have **Participation Status: Not participated**, **View Corrigendum**, **My Representations / Create Representation**, a 5-dot progress bar **Technical Bid → Offer Price → Upload Documents → EMD/EPBG → Verify & Esign**, and **Participate** | never |
| 3:44 | Participate → pop-up **"Compliance regarding Beneficial Ownership and Transfer of Technology"** | 3 questions: is bidder/OEM from a land-border country (Yes/No); any ToT arrangement with such entities (Yes/No); certify compliance (Yes). Save | never (legal) |
| 4:10 | **Bid Participation** page (`bidplus.gem.gov.in/bidding/sellerbid/participate/<id>`) | Left steps: **Catalogue Offering, Offer Price, Upload Documents, EMD/EPBG, Verify Bid Participation**. *Bid Details*: Bid Number, Bid Status, Bid Start / End Date, **Bid Validity (from end date): 30 days**, Bid Opening Date, links **TERMS AND CONDITIONS** and **CONSIGNEES / REPORTING OFFICER / DELIVERY LOCATION(S)**. *Buyer Details* (name masked in one bid), Ministry, Organisation, Department, Office. Item table: Item, **Category (with quadrant, e.g. "Broom Sticks (Q4)")**, Quantity, **SPECIFICATION** button. **Documents Required** list (Experience Criteria, Past Performance, Bidder Turnover, Certificate (Requested in ATC)) | prepare |
| 6:49 | **Consignees / Delivery Location(s)** pop-up | S.No., Consignee, **Address**, Category, Quantity, **Delivery Days** (15 in one bid, **60** in another). Captions: buyer and consignee can differ (bid from Delhi, deliver to Kerala); price the freight to the consignee | full (read it for him) |
| 7:52 | Another bid's Bid Details | **"Buyer Payment Status: Red"** shown on the right of Buyer Details. **Corrigendum Details** table: Modified On + "Bid extended to …", new Bid Opening Date. Bid validity 90 days on this one | full |
| 8:28 | **SPECIFICATION** expanded | Table: Category (Material / Classification / Dimensions…), Specification (e.g. Material of Handle, Type of Broom, Minimum overall weight), **Bid Requirement (Allowed Values)** — often a list of several allowed values ("200, 300, 400… or higher") | full (compare to his product) |
| 10:01 | Catalogue Offering → "Choose the product that you would like to offer" | "Only live catalogue matching the required specifications is shown." Buttons **UPLOAD NEW PRODUCT** and **CLICK HERE TO COMPARE WITH CURRENT CATALOGUE**; category filters pre-set to the bid's values. Message: **"You have no matching product available, please upload new product matching buyer requirements to participate"** | prepare |
| 12:48 | Market → Broom (V2) → left **Product Specifications** filters set to the bid's values (Material of handle = Plastic, Type = Soft broom with grass strips…) | 2,141 → 1,188 → fewer products. He picks one and pairs it (video 5). Captions: **exact match only** (bid asks 128 GB, a 256 GB phone can't bid). The new listing may take **from minutes up to 24 h to appear in the bid** (heavy in March) → list 1–2 days early | prepare (find matching listings) |
| 16:35 | Lyophilizer bid: Catalogue Offering done (✓) | "CHANGE CATALOGUE", CONTINUE. Note: **"The technical offering has been encrypted by the system"** | never |
| 17:01 | Custom-catalogue bid (e-cart / X-ray film) | "Choose this catalogue" cards with *Specification Document* links; then **Buyer Specification Document / Offered Specification Document** (Download), tick "I confirm the offered product meets the requirements in the buyer's specification document", Product Title / Make / Model, **Quantity You Can Fulfil**. Note: you may offer less than the bid quantity only if the bid allows it, and never below the minimum asked. **ENCRYPT & SAVE** | prepare |
| 17:26 | **Offer Price** | "Transaction charges would be applicable as per the Revenue Policy of GeM" (link). Yellow: **"Please enter price (inclusive of all taxes including GST)"**; per item unit price; **Total Offer Price** in words; "Encrypt and Save encrypts your financial quote; price visible only when the bid is opened. Take a screenshot for your records". Box: charges apply 1) when seller crosses ₹20 lakh merchandise value in a financial year (Annual Milestone Charges) 2) on all contracts ≥ ₹5 lakh after that | prepare (price advice) ; never (enter) |
| 19:31 | **Upload Documents** | One row per required document, each "Upload File (pdf, **max 10 MB**, max **100 pages**)": Experience Criteria, Past Performance, Bidder Turnover, **Certificate (Requested in ATC)** ("merge all ATC documents into a single file"), OEM Authorization Certificate, OEM Annual Turnover, **Additional Doc 1 (Requested in ATC)**. Bid Category. **"Are you manufacturing MSE for this product?" Yes/No** → Yes asks an MSE category certificate. Long note: false MSE / MII / EMD-exemption claims → rejection and action under GeM terms | prepare (the main job) |
| 20:20 | Bid PDF page 1 | Min. average annual turnover (3 yrs) **20 lakh**, **OEM average turnover** 20 lakh, years of past experience **2**, MSE exemption Yes, startup exemption No, documents required list, **Past Performance 20%** | full |
| 22:31 | **ATC page** (`fulfilment.gem.gov.in/contract/terms.jsp?bidra=…`) opened from TERMS AND CONDITIONS; same text on the last pages of the bid PDF ("Buyer Added Bid Specific Terms and Conditions") | Clauses: option clause ±25% quantity; bidder not bankrupt (undertaking); imported products need an Indian service office; OEM net worth positive; scope = supply only; **ISO 9001** required; **"Buyer uploaded ATC document: Click here to view the file"**; "Buyer added text based ATC clauses": a long list (ISO 14001/9001/45001, CVC, AIOTA, labour certs, GST cert, GSTR-3B/GSTR-1/GSTR-9, solvency ₹80 lakh, turnover certificate, balance sheet 3 yrs, toll-free number, escalation matrix…); turnover clause: CA/CS certificate or audited balance sheets | full (read and list documents) |
| 25:05 | Uploading the files | Each row turns to **Re-upload File** with the PDF name | never |
| 26:22 | EMD/EPBG step (not needed in this bid) → **VERIFY OTP/eSign/DSC** | Four declarations (land border; won't withdraw/modify during validity, info not false, will give PBG, GeM may debar; read GTC/STC/ATC/corrigenda; product meets specs), link **Bid Participation Draft Document**, tick "I agree…", buttons **VERIFY WITH OTP / ESIGN / DSC**; mobile OTP pop-up | never |
| 28:43 | Done | **"Bid Participation Participated"**, Bid No, Participated on …, **Bid Participation Document** (PDF: seller, bid details, technical offer "Encrypted", offer price as an encrypted string), **WITHDRAW BID**, VIEW MORE BIDS | never |
| 30:27 | Captions | Withdraw and re-submit **up to 3 times** before the deadline. His advice: bid even if you lack 2 of 10 documents and let the buyer decide | — |
| 31:06 | **Create Representation** (from a bid card) | Note: representation allowed **up to 4 days from bid publish**, **only once** per window; window can reopen if the buyer issues a corrigendum. Fields: Select Bid Section, Query (≤1000 chars), Add, Submit. "My Representations" table (Bid Section, Query, Submitted On). Captions: if the buyer doesn't answer, he can't open the bid until he extends it 3 days and replies | prepare (draft the question) |
| 32:18 | Talking head | Next: service bids | — |

### Changed since 2024

- Video (captions): ₹10k + GST each time he crosses ₹20 lakh, then **5%** on orders ≥ ₹5 lakh.
  On-screen box: Annual Milestone Charges at ₹20 lakh, then charges on contracts ≥ ₹5 lakh.
  **Today:** ₹10,000 + GST **once a year** at ₹20 lakh; then **0.30% only on orders above ₹10 lakh,
  max ₹3 lakh** (from 9 Aug 2024) [SFAQ, NEWS]. The 5% in the captions was wrong or a slip.
- Listing-to-bid delay: video says up to 24 h; GeM now says approval **normally 48 h** [GTC cl. 4(e)].
- Representation timing: §4a has the fuller rule (4 days for 10+-day bids, 1 day for 3–5-day, 2 days
  for 6–9-day; buyer must answer 72 h before bid end) [SFAQ].
- Bid validity, EMD, ePBG: see §4a (EMD none below ₹5 lakh; ePBG within 15 days of contract).
- 10 MB per file is on screen; §4a listed it as unchecked: **now seen on screen (2024)**, plus 100 pages.

### For the product

- **Buyer Payment Status (Red/Orange) is printed on the bid participation page** (logged in). Check
  whether the public bid PDF or list carries it too; if not, he can paste it, or the live tour can confirm.
- **Consignee address and delivery days** sit behind a pop-up and also in the bid PDF; we should
  extract them (HANDOFF §1 gap "consignee not extracted"). Delivery days varied 15 vs 60.
- **ATC lives at `fulfilment.gem.gov.in/contract/terms.jsp?bidra=…`** and at the end of the bid PDF,
  with a separate "buyer uploaded ATC document" file. That file is the gap in HANDOFF §2 step 1.
  The text ATC alone listed ~13 extra documents; a **document checklist per bid** is the biggest
  time-saver.
- **Exact spec match**: compare the bid's "Allowed Values" table against his listing's values and
  say which field fails, before he spends time.
- The document upload screen is the model for our checklist: one line per row, ≤10 MB and ≤100
  pages each, ATC certificates merged into one PDF.
- Remind: list the matching product **2+ days before** the bid ends.

---

## Video 11: Taking part in a custom bid (12:05)

Custom bid = buyer wants something with **no GeM category**. Buyer first makes a non-availability
report, then a custom catalogue with a spec PDF, then publishes the bid (open at least 21 days per
captions). The seller makes a **one-off catalogue for that one bid**.

### Screens in order

| Time | Screen | What is on it | AI |
|---|---|---|---|
| 3:21 | Seller bid list, **By Bid Type = Product Custom Bid/RAs**, category "Customitem prod…" | Same pink "select a category" box | never |
| 4:05 | Two bid PDFs side by side | **Category bid PDF:** a spec table "Specification / Specification Name / Bid Requirement (Allowed Values)" (e.g. bedside table: material, type, dimensions). Page 3 shows long standard clauses (MSE purchase preference: L1+15% band, 25% to MSE; MII Class-1/Class-2 local supplier; RA rules: H1 elimination exceptions) and an **Evaluation Method: Item-wise** table (Schedule, Estimated Value, Item/Category, Quantity) | full (we parse this PDF) |
| 5:02 | **Custom bid PDF** (Optical Elements (Q3), IIT Kanpur) | No spec table; instead a link to the buyer's **specification PDF** at `mkp.gem.gov.in/catalog_data/catalog_support_document/buyer_documents/.../SpecificationDocument/...pdf` (an annexure listing each optical part with numbers). Bid page 1 shows turnover 14 lakh, OEM turnover 28 lakh, experience 3 years | full (read the spec PDF) |
| 6:07 | Bid Participation page | **Buyer Payment Status: Red** again. Item "Optical Elements (Q3)", **Specification Document: Download**. Documents Required here: Experience, Past Performance, Bidder Turnover, Certificate (ATC), OEM Authorization, OEM Annual Turnover, Additional Doc 1 and 2 (ATC), **Financial Document** | prepare |
| 6:41 | "Choose the product…" → **UPLOAD NEW PRODUCT** (only way to make a custom catalogue) | Opens listing form in **Universal Category >> Universal Category…** | never |
| 7:20 | 1 General Information | Brand/OEM + tick "I certify that I am the OEM of the brand… or have authorisation…"; Golden Parameters: **Custom Specification** dropdown | prepare |
| 7:33 | 2 Catalogue Information | Model, Product Name, … "Is there any active/current bid for this catalogue?" → **Yes + Bid No. (mandatory for this category)**. A custom catalogue works **only for that bid** (not other bids, not direct purchase) | prepare |
| 8:28 | 3 Offering Quantity & Price | Country of origin, PPP-MII local content (with warning: false origin/MII = **grave incident**, account disabled), Make in India declaration, SKU, HSN, offer price (tentative) | prepare |
| 9:03 | 4 Product Specification | "Catalogue Document Guidelines: upload a document with the specs of the product you offer; buyer will use it to evaluate against his spec document". Upload **Specification Document** | prepare (draft a point-by-point compliance sheet) |
| 9:43 | 5 Upload Images → Review T&C → captcha → Publish | SUCCESS pop-up | never |
| 10:49 | Back in the bid → Choose the product | His new "Optical Elements ₹1,00,000" card appears **at once** (custom catalogues don't wait). Then Buyer Spec Document / Offered Spec Document, confirm tick, Product Title/Make/Model, Quantity you can fulfil, Encrypt & Save; rest as video 10 | never |

Captions tip: make your own spec PDF **and** add the buyer's spec PDF signed and stamped, merged into one file.

### Changed since 2024

- Nothing in §4a contradicts this. Minimum 21 days for custom bids not checked against an official source.

### For the product

- For custom bids the buyer's real requirements are in a **separate spec PDF** (link in the bid
  PDF). Our app should download and read it, same as the ATC file (HANDOFF §2 "read spec file").
- AI can draft the **compliance sheet** (buyer's line → his offer → complies yes/no) for him to sign.
- "Financial Document" can appear as an extra required document; include it in the checklist.

---

## Video 12: Bunch bids (several items) and service bids (8:42)

### Screens in order

| Time | Screen | What is on it | AI |
|---|---|---|---|
| 1:56 | Logged-in bid list, then `gem.gov.in` → public bid list | — | full |
| 3:13 | Bid PDF of a 2-item bid (Modular Table + Almirah Steel), "Bid Details" page | **Bid to RA enabled** No, **Type of Bid** Two Packet, **Primary product category**, **Time allowed for technical clarifications** 2 days, **Inspection required** No, **Estimated Bid Value** ₹17,25,000, **Evaluation Method: Total value wise evaluation**; **EMD Detail**: advisory bank, **EMD amount** ₹34,500; **ePBG Detail**: bank, **ePBG % 2.00**, **duration 12 months**; EMD exemption note (MSE makers / startups, upload proof; traders not exempt) | full (we parse this PDF) |
| 3:33 | Same PDF, later pages | Past-performance clause (40% of bid quantity in one of last 3 years, to a govt org/PSU/listed company); per-item spec tables ("As per GeM Category Specification"); **consignee table: Reporting Officer, Address, Quantity, Delivery Days (15)**; Buyer Added ATC: bidder and OEM turnover clauses, **Service & Support: functional service centre in each consignee state** (or set one up within 30 days of award; payment only after proof), **dedicated toll-free number** | full |
| 3:56 | 5-item bid PDF | **Evaluation Method: Item wise** table with Schedule 1–5, estimated value, item, quantity; items marked **"(Under PAC)"** with fixed Make/Model; MII purchase preference No, MSE purchase preference Yes; **"Details of the Competent Authority approval for PAC"** (name, designation, approval number, date, "View Document") | full |
| 5:10 | Participate (item-wise bid) → Catalogue Offering | Note: **"Seller can participate in one or more schedules… EMD % will apply on the selected schedules only."** Table: Schedule Name, Category, Quantity, Consignee VIEW, tick boxes, SELECT ALL SCHEDULES, **SAVE SELECTED SCHEDULES** (he ticks 2, 4, 5) | prepare (which schedules he can supply) |
| 5:53 | Service bid: category **Cab and Taxi Hiring** | 574 bids; e.g. "Monthly Basis Cab & Taxi Hiring Services – Sedan; 2000 km × 320 hours; Local 24×7", Number of vehicles 1, Buyer Payment Status shown | never |
| 6:59 | Service **Catalogue Offering** | Table: **Specification / Bid Requirement / Offered** (dropdown per row): vehicle type Sedan vs Hatchback, type of car (pick ≥3: Dzire, Xcent, Tigor), usage 2000 km × 320 h, local 24×7, model year 2021–23, km travelled ≤25,000, A/C, hilly + plain area, fuel any. **ENCRYPT & SAVE**. No new catalogue needed per bid for services | prepare (fill offered column from his fleet) |
| 7:21 | Done | "The technical offering has been encrypted…", CHANGE CATALOGUE, CONTINUE; then price, documents, OTP as video 10 | never |

Captions: total-value bids need every item; item-wise bids let him choose; service bids always need all services.

### Changed since 2024

- EMD shown (2% here) fits [GTC cl. 4(m)] range. ePBG 2% for 12 months: buyer may pick up to 5%
  (GFR 3–5%) [GTC cl. 7], so 2% on a 2024 bid is lower than today's GFR range; not re-checked.

### For the product

- From the bid PDF we can show at once: **total-value vs item-wise** (can he bid on part?),
  **PAC items** (fixed brand/model: only that model can bid), **EMD amount**, **ePBG % and months**,
  **estimated bid value**, **inspection required**, **service-centre-in-each-state** and toll-free
  rules in ATC. Some are already parsed (HANDOFF §1); check which are missing.
- For item-wise bids, list the schedules his catalogue can match, so he ticks only those.

---

## Video 13: BOQ bids (no catalogue needed) (8:18, 360p)

BOQ (bill of quantity) bid = buyer needs **5 or more** items that have no GeM category, in one bid.
The only bid type where the seller **lists nothing first**. Captions: don't expect BOQ for items that
do have a category.

### Screens in order

| Time | Screen | What is on it | AI |
|---|---|---|---|
| 2:09 | Seller bid list, category **"BOQ"** selected | BOQ bids show up like others | never |
| 2:31 | BOQ bid PDF | Page 1: Item Category = a list (self inking stamp ink, …ink1, ink2…), **BOQ Title**, Bid to RA No, Type Two Packet, Primary product category, technical clarification 2 days, inspection No, Evaluation **Total value wise**. Per item: "(Minimum 50% and 20% local content for Class 1 and Class 2 local supplier)", links **Specification Document: View File** and **BOQ Detail Document: View File**; consignee table with Delivery Days (10) | full |
| 2:45 | Buyer's spec PDF (`mkp.gem.gov.in/uploaded_documents/.../BoqDocument/...`) | A one-page letter: table of items (particulars, spec, colour, quantity) + notes (e.g. "only participants ready to supply", "adequate experience") | full (read it) |
| 3:13 | **BOQ Detail Document** (spreadsheet) | Columns: Item Number, Item Title, Item Description, Item Quantity, Unit of Measure, Consignee ID, Delivery Period (days). Captions: sellers used to fill prices in this sheet; since ~2023 not needed, it is for reading only | full |
| 3:51 | Bid Participation → Catalogue Offering | Each item row has **SELECT CATALOGUE** → "Please enter the item details": **Make, Model, HSN Code** → SAVE AND CONTINUE (row turns to CHANGE CATALOGUE). Captions: these **go onto the purchase order** exactly, so be correct. Documents required here: Certificate (ATC), **Compliance of BoQ specification and supporting document** | prepare (draft make/model/HSN list) |
| 5:25 | Offer Price | Unit price (incl. all taxes) per item; site shows the total | prepare |
| 6:13 | Representation pop-up | Here the note says **"up to 2 days from bid publish"** (a shorter bid); one per window; reopens on corrigendum. Another bid shows only "My Representations" (window closed) | prepare |
| 7:38 | Talking head | Next: results and competitors' prices | — |

### Changed since 2024

- The 2-day representation window on screen matches the official rule for 6–9-day bids [SFAQ].
- Nothing else here conflicts with §4a.

### For the product

- BOQ bids are the easiest to bid on (no listing). Good alert target for a small seller: search
  **BOQ Title** (video 9) for his product words.
- The BOQ detail sheet is a clean, machine-readable item list; parse it to tell him which lines he
  can supply.
- AI can prepare the **Make / Model / HSN** list per line (it ends up on the PO, so he checks it).

---

## Video 14: Getting a direct purchase order (filmed in Ladakh) (10:42)

First 6 minutes: talking head outdoors. Direct purchase is meant to be "buyer picks the cheapest
listing"; sellers use it when a **known buyer** wants to order from them. Before starting he must
know three things: **exact price, exact delivery location, exact quantity**.

### Screens in order

| Time | Screen | What is on it | AI |
|---|---|---|---|
| 6:23 | Market → **Plain Copier Paper (V2) as per IS 14490 (Q4 Category)** | 1,247 products, from ₹70 | full (public) |
| 6:37 | Sort **Price: High to Low** | Top listings ₹500 (OEM, VA). Check: can his target price (₹385) sit in this category's range at all? | full |
| 7:28 | Left filters → **Product Specifications** | BIS, grammage, ECO-mark, "agree to provide advance samples…", number of sheets in a ream, **Sizes** (A4), BIS marked, test report from NABL/ILAC lab… He ticks **A4** → 789 products | full |
| 7:39 | Result cards around his price (₹395, ₹310, ₹300) | Rule in captions: if the matching listing shows **more** than his target → copy it ("Sell this item"), set price/stock/location, then **send the product link to the buyer**. If it shows **less** → check where that cheaper price applies | full / prepare |
| 8:05 | Product page (Bindals A4 ₹395, MRP ₹475; country of origin "Not Declared") | MRP decides the lowest he can go (≥10% below MRP) | full |
| 8:22 | **VIEW ALL SELLERS** → **Other Sellers** for RADEX A4 80 GSM | Rows: ₹359 for district Jalpaiguri (WB) + pin 735232; ₹305 Dehradun district; ₹440 Delhi; ₹320 Andhra Pradesh… each with OEM-verified flags, stock, min qty. He checks no one lists **below his price for the buyer's location** (Meghalaya) → he can win it | full (public) |
| 10:16 | Talking head | Next video promised: ₹25k–₹5 lakh direct purchase (not in this playlist) | — |

### Changed since 2024

- Video: direct up to **₹25,000** with no comparison; ₹25k–₹5 lakh needs 3-way comparison; tender
  above ₹5 lakh. **Today:** direct up to **₹50,000**; **₹50k–₹10 lakh** = L1 among ≥3 sellers/OEMs;
  above ₹10 lakh bid/RA [GTC cl. 4, BFAQ].
- Direct/L1 orders are auto-accepted except red-flag buyers/freight-heavy (120 h to decide);
  declining freezes stock for 15 days [SFAQ] (not in the video).
- MRP rule (≥10% below) still true [SFAQ].

### For the product

- A **"win this direct order" helper** is all public data and read-only: given category, spec
  (e.g. A4), buyer's district/state and target price, scan the category sorted by price, open
  "Other Sellers" for the closest listings, and tell him whether anyone undercuts him **for that
  location**, and the lowest price he can list (MRP − 10%). He then lists and sends the link himself.
- Warn: once listed for that location he must deliver any direct order from it (video 5 warning).

---

## Video 15: Bid results, competitors' prices, Push Button Procurement, contracts (10:48)

### Screens in order

| Time | Screen | What is on it | AI |
|---|---|---|---|
| 3:25 | Seller bid list → tick **Participated Bids** | Extra filter **By Bid/RA Status: Technical Evaluated, Financial Evaluated, Bid/RA Awarded**. Cards show Status (e.g. Technical Evaluation, Bid Award), **Technical Status: Qualified / Disqualified 👁**, links **BID Document**, **Participation Document**, progress Technical Evaluation → Financial Evaluation → Bid Award, **View BID Results** | never (login) |
| 4:19 | **Bid result page** (`bidplus.gem.gov.in/bidding/bid/getBidResultView/<id>`) | 1 Bid Details (status, quantity, dates, validity, avg turnover asked, experience asked), Buyer Details, **2 Technical Evaluation: "List of Sellers Participated"**: S.No, **Seller Name**, Offered Item (make/model/title), Participated On, **EMD Status** (e.g. "Registered with designated Agency/Authority", "Start-up"), MSE/MII status, **Status Qualified/Disqualified** (eye icon shows the buyer's reason), Specification view, Clarifications, **Challenge/Representation**; **3 Financial Evaluation** (prices and rank) | full (public, see below) |
| 4:47 | Disqualified row | Captions: a **challenge window of 2 days**, once; buyer may or may not reconsider. Advisory: accepting/rejecting is the buyer's call, GeM has no role | prepare (draft challenge text) |
| 5:40 | Logged out: `bidplus.gem.gov.in/all-bids` → tick **Bid/RA Status** | 18,039 records with Status Not Evaluated / Technical Evaluation / Financial Evaluation / Bid Award; buttons **View Bid Results** and **View RA Results**. Keyword "almirah" → past almirah bids; open one → same result page as above, **without login** | full (public) |
| 6:58 | Seller dashboard → **Push Button Procurement** (`bestprice.gem.gov.in/…`) | **Product PBP Notice** list: PBP Notice Number (GEM/2024/PBP/…), item (e.g. Laptop – Notebook), quantity, ministry, organisation, department/address, PBP Notice Status (Published / Cancelled), create and end date, **Offer Product**. Captions: experimental mode, open only **3 days**, **no documents**, only some categories; buyer uses it when listed prices look too high | prepare (alert); never (offer) |
| 8:07 | `gem.gov.in` → **View Contracts** (`gem.gov.in/view_contracts`) | Search by date range (+ bid number), category; **captcha required**. Each contract: Contract No (GEMC-…), Status (Order Accepted / Fulfilment in Progress / Waiting for Seller Payment), Organisation type and name, ministry, department, office zone, buyer designation, **Buying Mode: Direct or Bid/RA** (+ bid number), contract date, total; product, **brand, model, ordered quantity, price**. Contract PDF downloadable: buyer, financial approval, paying authority, **seller name/company**, GST note ("GST invoice to be raised in the name of the buyer"), product table | full to read by hand; **not for a bot (captcha)** |
| 9:48 | Talking head | Next: direct purchase (video 14 in this playlist) | — |

### Changed since 2024

- Challenge: once, within **48 hours after technical evaluation** [SFAQ]: matches "2 days".
- "Waiting for Seller Payment" status on a contract is likely the transaction-charge step (must pay
  before accepting/invoicing) [SFAQ]; not explained in the video.

### For the product

- **Past results are public without login**: `bidplus.gem.gov.in/all-bids` with Bid/RA Status, then
  `…/getBidResultView/<id>` lists every bidder, qualified or not, and (financial tab) their prices.
  This is the source for HANDOFF §2 "past winning (L1) prices" and for "who are my competitors".
  Keep the same safety limits as today's search (read-only, slow, daily budget).
- **View Contracts needs a captcha**: our app must **not** automate it (the "no CAPTCHA, no
  scraping-past-protection" rule). He can look up a contract himself, or paste a contract PDF for
  the AI to read.
- **Push Button Procurement notices** are short (3 days) and have no paperwork: worth an alert if he
  sells in a PBP category. Where they show without login is not checked.
- After a rejection, the AI can read the buyer's reason (he pastes it) and draft the one-time
  challenge within 48 h.

---

## What the 15 videos add for the product (summary)

New compared with HANDOFF §4/§4a, all seen on screen:

1. **Public pages we can read without login** (read-only, slow, within today's limits):
   category search with quadrants (`mkp.gem.gov.in/search?q=`), category pages with prices and
   filters, Browse All Categories / Brands, a product's **Other Sellers** (price per location),
   bid list filters and Advance Search (category, ministry/state, consignee city, BOQ title),
   bid results with all bidders (`getBidResultView`). Not for a bot: **View Contracts** (captcha).
2. **Bid documents hold more than we read today:** consignee address + delivery days, EMD amount,
   ePBG % and months, evaluation method (total vs item-wise), PAC items, inspection, estimated
   value, MSE/MII preference, plus **ATC text** (`fulfilment.gem.gov.in/contract/terms.jsp`),
   the **buyer-uploaded ATC file**, the **custom/BOQ spec PDF** and the **BOQ detail sheet**.
3. **Buyer Payment Status (Red/Orange)** appears on the logged-in bid participation page.
4. **Exact-spec matching** is the real gate: the bid's "Allowed Values" table vs his listing.
   Listing a match takes up to 48 h to reach the bid → alerts must come early.
5. **Prepare-only helpers** the screens make obvious: per-bid document checklist (≤10 MB,
   ≤100 pages per file, ATC certificates merged), spec-sheet → GeM dropdown mapping for new
   listings, listing pre-check (photos, MRP proof, brand/model), compliance sheet for custom bids,
   Make/Model/HSN list for BOQ, buyer questions (representation) and challenge drafts,
   "can I win this direct order at this location?" check.
6. **Still never for the AI:** anything after login that submits, declares, pays or uses an OTP
   (sign-up, profile, listing publish, bid submit, MII/land-border declarations, caution money).

Not covered by the playlist (unchanged from HANDOFF §4): accepting orders, delivery, invoices,
payments, ePBG upload, ₹50k–₹10 lakh L1 purchase, ratings, incidents. These are for the live tour.
