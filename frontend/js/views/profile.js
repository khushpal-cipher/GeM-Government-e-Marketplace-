import { el, notice, splitList } from "../dom.js";

export const EMPTY_PROFILE = {
  business_name: "",
  is_mse: false,
  is_startup: false,
  is_oem: false,
  annual_turnover_rupees: null,
  years_experience: null,
  categories: [],
  certifications: [],
  states: [],
  ignore_words: [],
  bid_order: "match",
  gem_registered_on: null,
  itr_filed_on_gem: null,
  pfms_bank_verified: null,
  oem_products: [],
  own_made_products: [],
  products: [],
};

// "A4 paper: GSM = 80; Size = A4" per line <-> {name, specs}. Up to 5 products, 15 specs each (the server checks too).
export function parseProducts(text) {
  return text.split("\n").map((line) => line.trim()).filter(Boolean).map((line) => {
    const cut = line.indexOf(":");
    const specs = {};
    if (cut >= 0) {
      for (const pair of line.slice(cut + 1).split(";")) {
        const eq = pair.indexOf("=");
        if (eq > 0 && pair.slice(eq + 1).trim()) specs[pair.slice(0, eq).trim()] = pair.slice(eq + 1).trim();
      }
    }
    return { name: (cut >= 0 ? line.slice(0, cut) : line).trim(), specs };
  });
}

export function formatProducts(products) {
  return products.map((p) => {
    const pairs = Object.entries(p.specs).map(([k, v]) => `${k} = ${v}`).join("; ");
    return pairs ? `${p.name}: ${pairs}` : p.name;
  }).join("\n");
}

function field(labelText, input, hint) {
  return el("div", {}, el("label", { for: input.id }, labelText), input, hint ? el("div", { class: "hint" }, hint) : null);
}

function checkbox(id, labelText, checked) {
  const input = el("input", { type: "checkbox", id, checked });
  return { input, node: el("label", { class: "check", for: id }, input, labelText) };
}

// "10,00,000", "10 lakh", "1.5 crore", "₹ 25,50,000" -> rupees; NaN when it can't be read.
// A number box would silently save "10,00,000" as blank in Safari.
export function parseRupees(text) {
  const m = text.toLowerCase().replace(/,/g, "").trim()
    .match(/^(?:₹|rs\.?|inr)?\s*(\d+(?:\.\d+)?)\s*(lakhs?|lacs?|crores?|cr)?$/);
  if (!m) return NaN;
  const unit = !m[2] ? 1 : m[2].startsWith("c") ? 1e7 : 1e5;
  return Math.round(Number(m[1]) * unit);
}

export const inr = (rupees) => `₹${rupees.toLocaleString("en-IN")}`;

// A yes / no / "I don't know" box: unknown is saved as null, never as "no".
function triState(id, value) {
  const select = el("select", { id },
    el("option", { value: "" }, "I don't know"), el("option", { value: "yes" }, "Yes"), el("option", { value: "no" }, "No"));
  select.value = value == null ? "" : value ? "yes" : "no";
  return { select, get: () => (select.value === "" ? null : select.value === "yes") };
}

export async function renderProfile(container, _params, api) {
  const profile = { ...EMPTY_PROFILE, ...((await api.getProfile()) || {}) };
  const warnings = (await api.getProfileWarnings()) || [];
  const specNames = ((await api.getSpecNames().catch(() => [])) || []).slice(0, 12);

  const name = el("input", { type: "text", id: "business_name", value: profile.business_name });
  const turnover = el("input", { type: "text", inputmode: "decimal", id: "turnover",
    placeholder: "e.g. 25,00,000 or 25 lakh",
    value: profile.annual_turnover_rupees == null ? "" : profile.annual_turnover_rupees.toLocaleString("en-IN") });
  const turnoverHint = el("div", { class: "hint" }, "Average of the last 3 financial years.");
  turnover.addEventListener("input", () => {
    const rupees = parseRupees(turnover.value);
    turnoverHint.textContent = !turnover.value.trim() ? "Average of the last 3 financial years."
      : Number.isNaN(rupees) ? "Can't read this yet. Write it like 25,00,000 or 25 lakh." : `= ${inr(rupees)}`;
  });
  const years = el("input", { type: "text", inputmode: "numeric", id: "years", value: profile.years_experience ?? "" });
  const categories = el("textarea", { id: "categories" }); categories.value = profile.categories.join(", ");
  const certs = el("textarea", { id: "certs" }); certs.value = profile.certifications.join(", ");
  const states = el("textarea", { id: "states" }); states.value = profile.states.join(", ");
  const registered = el("input", { type: "date", id: "registered", value: profile.gem_registered_on || "" });
  const itr = triState("itr", profile.itr_filed_on_gem);
  const pfms = triState("pfms", profile.pfms_bank_verified);
  const oemProducts = el("textarea", { id: "oem_products" }); oemProducts.value = profile.oem_products.join(", ");
  const ownMade = el("textarea", { id: "own_made" }); ownMade.value = profile.own_made_products.join(", ");
  const products = el("textarea", { id: "products", rows: 5 }); products.value = formatProducts(profile.products);
  const mse = checkbox("is_mse", "Registered MSE (Udyam)", profile.is_mse);
  const startup = checkbox("is_startup", "DPIIT-recognised startup", profile.is_startup);
  const oem = checkbox("is_oem", "We are the OEM (manufacturer), not a reseller", profile.is_oem);

  const status = el("div");
  const save = el("button", { type: "submit" }, "Save profile");

  const form = el("form", { class: "card" },
    el("div", { class: "grid-2" },
      field("Business name", name),
      el("div", {}, el("label", { for: "turnover" }, "Annual turnover (₹)"), turnover, turnoverHint),
      field("Years of experience", years),
      el("div", {}, el("label", {}, "Status"), mse.node, startup.node, oem.node),
      field("Products you sell", categories, "Comma-separated, as GeM names them. Also on the Find bids page."),
      field("Certifications held", certs, "For example: ISO 9001, BIS"),
      field("States you can deliver to", states, "Comma-separated."),
      field("Date you registered on GeM", registered),
      field("Income tax return (ITR) filed on GeM?", itr.select),
      field("Bank account PFMS-verified on GeM?", pfms.select),
      field("Products where you are the OEM", oemProducts, "Comma-separated. The rest count as resold."),
      field("Items you make yourself", ownMade, "MSE EMD exemption applies only to these."),
      field("Your main products and key specs", products,
        "Up to 5 lines, up to 15 specs each, like: A4 paper: GSM = 80; Size = A4." +
        (specNames.length ? ` Names GeM bids use: ${specNames.join(", ")}.` : "")),
    ),
    el("div", { class: "row", style: "margin-top:16px" }, save),
    status,
  );

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const rupees = turnover.value.trim() ? parseRupees(turnover.value) : null;
    if (Number.isNaN(rupees)) {
      status.replaceChildren(notice("bad", `Turnover: couldn't read “${turnover.value.trim()}”. Write it like 25,00,000 or 25 lakh.`));
      return;
    }
    if (years.value.trim() && !/^\d+$/.test(years.value.trim())) {
      status.replaceChildren(notice("bad", "Years of experience: write a whole number, like 3."));
      return;
    }
    save.disabled = true;
    try {
      await api.saveProfile({
        ...profile,
        business_name: name.value.trim(),
        is_mse: mse.input.checked,
        is_startup: startup.input.checked,
        is_oem: oem.input.checked,
        annual_turnover_rupees: rupees,
        years_experience: years.value.trim() ? Number(years.value.trim()) : null,
        categories: splitList(categories.value),
        certifications: splitList(certs.value),
        states: splitList(states.value),
        gem_registered_on: registered.value || null,
        itr_filed_on_gem: itr.get(),
        pfms_bank_verified: pfms.get(),
        oem_products: splitList(oemProducts.value),
        own_made_products: splitList(ownMade.value),
        products: parseProducts(products.value),
      });
      status.replaceChildren(notice("ok", "Saved. Bid verdicts now use this profile."));
    } catch (error) {
      status.replaceChildren(notice("bad", error.message));
    } finally {
      save.disabled = false;
    }
  });

  container.append(
    el("h1", {}, "Seller profile"),
    el("div", { class: "subtle" },
      "Used to check each bid. Stored only on this computer and never sent to GeM or to the AI."),
    ...warnings.map((text) => notice("bad", text)),
    form,
  );
}
