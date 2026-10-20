import { el, notice } from "../dom.js";

// Order tracker — he pastes or types his order details. App never logs in to GeM.
// Stages: Contract Placed → Dispatched → Received (CRAC) → Payment Completed.
// Deadlines from GeM GTC v1.29 (HANDOFF §4a).
export async function renderOrders(container, _params, api) {
  const list = el("div");
  const status = el("div");
  const pasteStatus = el("div");
  const pastePreview = el("div");

  async function refresh() {
    const orders = await api.getOrders();
    if (!orders.length) {
      list.replaceChildren(el("div", { class: "subtle" }, "No orders tracked yet."));
      return;
    }
    list.replaceChildren(...orders.map(orderCard));
  }

  function stageBadge(s) {
    const map = {
      CONTRACT_PLACED: ["warn", "Contract Placed"],
      DISPATCHED: ["warn", "Dispatched"],
      RECEIVED: ["ok", "CRAC Received"],
      PAYMENT_COMPLETED: ["ok", "Payment Done"],
    };
    const [cls, label] = map[s] || ["warn", s];
    return el("span", { class: `badge ${cls}` }, label);
  }

  function deadlineRow(d) {
    const cls = d.is_overdue ? "bad" : (d.severity === "warn" ? "warn" : "info");
    const pen = d.penalty_rupees ? ` · LD penalty: ₹${d.penalty_rupees.toLocaleString("en-IN")}` : "";
    return el("div", { class: "card", style: "margin:4px 0;padding:8px 12px;" },
      el("div", { class: "row" },
        el("strong", {}, d.name),
        el("span", { class: `badge ${cls}` }, d.due_text)),
      el("div", { class: "hint" }, `Action: ${d.action}${pen}`),
      el("div", { class: "hint" }, d.note));
  }

  function chargesRow(c) {
    if (!c.total_charges) return null;
    const parts = [];
    if (c.milestone_charge) parts.push(`Milestone ₹${c.milestone_charge.toLocaleString("en-IN")} + GST ₹${c.milestone_gst.toLocaleString("en-IN")}`);
    if (c.transaction_charge) parts.push(`Transaction 0.30% = ₹${c.transaction_charge.toLocaleString("en-IN")} + GST ₹${c.transaction_gst.toLocaleString("en-IN")}`);
    if (c.tds_applicable) parts.push("TDS 2% may apply (charges > ₹30,000)");
    return el("div", { class: "card", style: "margin:4px 0;padding:8px 12px;background:#fafafa;" },
      el("strong", {}, `GeM Charges: ₹${c.total_charges.toLocaleString("en-IN")}`),
      el("div", { class: "hint" }, parts.join(" · ")));
  }

  function orderCard(o) {
    const card = el("div", { class: "card" });

    const updateForm = el("form", { style: "display:none;margin-top:10px;" });
    const toggleUpdate = el("button", { type: "button", class: "secondary" }, "Update stage");
    toggleUpdate.addEventListener("click", () => {
      updateForm.style.display = updateForm.style.display === "none" ? "block" : "none";
    });

    const draftBtn = el("button", { type: "button", class: "secondary" }, "Incident draft");
    draftBtn.addEventListener("click", async () => {
      const res = await api.getOrderIncidentDraft(o.id);
      const ta = card.querySelector(".incident-draft");
      if (ta) { ta.remove(); return; }
      const box = el("div", { class: "incident-draft card", style: "margin-top:8px;" },
        el("label", {}, "Payment delay incident draft:"),
        el("textarea", { rows: "8", style: "width:100%;font-family:monospace;font-size:13px;", readonly: "true" }, res.draft));
      card.append(box);
    });

    // Stage update fields
    const stageFields = [
      ["epbg_submitted_at", "ePBG submitted on", "date"],
      ["dispatched_at", "Dispatched on", "date"],
      ["proof_of_delivery_at", "Proof of delivery on", "date"],
      ["crac_at", "CRAC received on", "date"],
      ["payment_at", "Payment received on", "date"],
      ["buyer_request_at", "Buyer request received on", "date"],
    ];
    const inputs = {};
    stageFields.forEach(([key, label, type]) => {
      const inp = el("input", { type, value: o[key] || "" });
      inputs[key] = inp;
      updateForm.append(el("div", { style: "margin-bottom:6px;" },
        el("label", { style: "display:block;font-size:13px;" }, label), inp));
    });
    const saveStage = el("button", { type: "submit" }, "Save");
    updateForm.append(el("div", { class: "row", style: "margin-top:8px;" }, saveStage));
    updateForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const updates = {};
      Object.entries(inputs).forEach(([k, inp]) => { if (inp.value) updates[k] = inp.value; });
      await api.updateOrder(o.id, updates);
      refresh();
    });

    card.append(
      el("div", { class: "row" },
        el("strong", {}, o.contract_number),
        stageBadge(o.status),
        el("div", { class: "row" }, toggleUpdate, draftBtn)),
      el("div", { class: "hint" }, `Value: ₹${o.order_value_rupees.toLocaleString("en-IN")}` +
        (o.buyer_department ? ` · ${o.buyer_department}` : "") +
        ` · Expected delivery: ${o.expected_delivery_date}`),
      ...o.deadlines.map(deadlineRow),
      chargesRow(o.charges),
      updateForm,
    );
    return card;
  }

  // --- Add new order ---
  const pasteArea = el("textarea", { id: "order-paste", rows: "5", placeholder: "Paste from GeM Orders screen…" });
  const readBtn = el("button", { type: "submit" }, "Read it");
  const pasteForm = el("form", { class: "card" },
    el("label", { for: "order-paste" }, "Paste order details from GeM"),
    el("div", { class: "hint" }, "Open GeM → Orders → click the contract number → copy the details. Stays on this computer."),
    pasteArea,
    el("div", { class: "row", style: "margin-top:8px;" }, readBtn),
    pasteStatus, pastePreview);

  pasteForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    pasteStatus.replaceChildren(); pastePreview.replaceChildren();
    const parsed = await api.parseOrderPaste(pasteArea.value).catch(() => null);
    if (!parsed) {
      pasteStatus.replaceChildren(notice("bad", "No contract number found. Is this from the GeM Orders screen?"));
      return;
    }
    // Show editable fields to confirm before saving
    const fields = {
      contract_number: el("input", { type: "text", value: parsed.contract_number }),
      contract_date: el("input", { type: "date", value: parsed.contract_date }),
      order_value_rupees: el("input", { type: "number", value: parsed.order_value_rupees }),
      expected_delivery_date: el("input", { type: "date", value: parsed.expected_delivery_date }),
      epbg_percent: el("input", { type: "number", step: "0.1", value: parsed.epbg_percent || "" }),
      buyer_department: el("input", { type: "text", value: parsed.buyer_department || "" }),
    };
    const labels = {
      contract_number: "Contract Number", contract_date: "Contract Date",
      order_value_rupees: "Order Value (₹)", expected_delivery_date: "Expected Delivery Date",
      epbg_percent: "ePBG %", buyer_department: "Department",
    };
    const confirmCard = el("div", { class: "card" },
      notice("warn", "Please check these details before saving."),
      el("div", { class: "grid-2" },
        ...Object.entries(fields).map(([k, inp]) =>
          el("div", {}, el("label", {}, labels[k]), inp))));
    const confirmBtn = el("button", { type: "button" }, "Save order");
    confirmBtn.addEventListener("click", async () => {
      const body = {
        contract_number: fields.contract_number.value,
        contract_date: fields.contract_date.value,
        order_value_rupees: parseInt(fields.order_value_rupees.value, 10),
        expected_delivery_date: fields.expected_delivery_date.value,
        epbg_percent: parseFloat(fields.epbg_percent.value) || null,
        buyer_department: fields.buyer_department.value || null,
      };
      await api.saveOrder(body);
      pasteArea.value = ""; pastePreview.replaceChildren();
      pasteStatus.replaceChildren(notice("ok", "Order saved."));
      refresh();
    });
    pastePreview.append(confirmCard, confirmBtn);
  });

  container.append(
    el("h1", {}, "Order Tracker"),
    el("div", { class: "subtle" }, "Tracks your orders: delivery date, CRAC, payment and ePBG deadlines. You log in to GeM yourself."),
    pasteForm,
    el("h2", {}, "Active orders"),
    list);
  await refresh();
}
