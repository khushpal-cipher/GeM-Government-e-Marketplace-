import { el, notice } from "../dom.js";

// The daily GeM check. He opens his own GeM account and pastes; the app never logs in. Each pasted
// item is shown back (number, date) so he can fix it before it becomes an alert.
export async function renderToday(container, _params, api) {
  const kinds = await api.getAlertKinds();
  const list = el("div");
  const status = el("div");
  const preview = el("div");

  async function refresh() {
    const alerts = await api.getAlerts();
    list.replaceChildren(...(alerts.length ? alerts.map(alertCard) : [el("div", { class: "subtle" }, "Nothing waiting.")]));
  }

  function renderShortfallReply(reply, target) {
    const existing = target.querySelector(".shortfall-box");
    if (existing) existing.remove();
    const replyBox = el("div", { class: "card shortfall-box", style: "margin-top: 10px; background: #fdfdfd; border: 1px solid #d1d5db;" },
      el("div", { class: "row" },
        el("strong", {}, `Shortfall Reply${reply.bid_number ? `: ${reply.bid_number}` : ""}`),
        reply.due_text ? el("span", { class: "badge warn" }, reply.due_text) : null),
      el("div", { style: "margin: 8px 0;" },
        el("strong", {}, "Requested documents:"),
        el("ul", { style: "margin: 4px 0 10px 20px; padding: 0;" },
          ...reply.documents.map(d => el("li", { style: "margin-bottom: 4px;" },
            el("strong", {}, d.name),
            el("span", { class: `badge ${d.in_profile === true ? "ok" : (d.in_profile === false ? "bad" : "warn")}`, style: "margin-left: 6px;" },
              d.in_profile === true ? "In profile" : (d.in_profile === false ? "Missing from profile" : "Check manual")),
            el("div", { class: "hint" }, `${d.profile_note} (Quote: "${d.quote}")`))))),
      el("label", {}, "Covering note draft:"),
      el("textarea", { rows: "8", style: "width: 100%; font-family: monospace; font-size: 13px;", readonly: "true" }, reply.draft),
      el("div", { class: "row", style: "margin-top: 8px;" },
        el("button", {
          type: "button",
          click: (e) => {
            navigator.clipboard.writeText(reply.draft);
            e.target.textContent = "Copied!";
            setTimeout(() => { e.target.textContent = "Copy draft"; }, 2000);
          }
        }, "Copy draft"),
        el("button", { type: "button", class: "secondary", click: () => replyBox.remove() }, "Close"))
    );
    target.append(replyBox);
  }

  function alertCard(a) {
    const card = el("div", { class: "card" });
    const done = el("button", { type: "button", class: "secondary" }, "Done");
    done.addEventListener("click", async () => { await api.finishAlert(a.id); refresh(); });
    const actions = [done];
    if (a.kind === "clarification") {
      const draft = el("button", { type: "button", class: "secondary" }, "Draft reply");
      draft.addEventListener("click", async () => {
        const reply = await api.getShortfallReply(a.text, a.ref, a.due);
        renderShortfallReply(reply, card);
      });
      actions.unshift(draft);
    }
    card.append(
      el("div", { class: "row" },
        el("strong", {}, `${a.label}${a.ref ? `: ${a.ref}` : ""}`),
        el("span", { class: `badge ${a.overdue ? "bad" : "warn"}` }, a.due_text),
        el("div", { class: "row" }, ...actions)),
      el("div", { class: "hint" }, `Do it on GeM: ${a.where}`),
      el("div", { class: "hint" }, `If missed: ${a.if_missed}`),
      a.text ? el("div", { class: "hint" }, a.text.slice(0, 300)) : null);
    return card;
  }

  const kind = el("select", { id: "kind" }, ...Object.entries(kinds).map(([k, v]) => el("option", { value: k }, v.label)));
  const ask = el("div", { class: "hint" });
  const paste = el("textarea", { id: "paste", rows: "6", placeholder: "Paste here" });
  const show = () => { ask.textContent = `Open on GeM and copy: ${kinds[kind.value].ask}`; };
  kind.addEventListener("change", show); show();

  const check = el("button", { type: "submit" }, "Read it");
  const form = el("form", { class: "card" },
    el("label", { for: "kind" }, "What did you find on GeM?"), kind, ask,
    el("label", { for: "paste" }, "Paste it"), paste,
    el("div", { class: "hint" }, "Stays on this computer. Nothing is sent to GeM."),
    el("div", { class: "row", style: "margin-top:12px" }, check), status, preview);

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    status.replaceChildren(); preview.replaceChildren();
    const items = await api.previewAlerts(kind.value, paste.value);
    if (!items.length) { status.replaceChildren(notice("bad", "Nothing pasted.")); return; }
    const rows = items.map((item) => {
      const ref = el("input", { type: "text", value: item.ref, placeholder: "bid or contract number" });
      const due = el("input", { type: "date", value: item.due || "" });
      const rowCard = el("div", { class: "card" });
      const headerRow = el("div", { class: "row" },
        el("strong", {}, item.ref || "Pending item"));
      if (kind.value === "clarification") {
        const draftBtn = el("button", { type: "button", class: "secondary" }, "Draft reply");
        draftBtn.addEventListener("click", async () => {
          const reply = await api.getShortfallReply(item.text, ref.value, due.value || null);
          renderShortfallReply(reply, rowCard);
        });
        headerRow.append(draftBtn);
      }
      rowCard.append(
        item.unclear ? notice("warn", `Please check: ${item.unclear}.`) : null,
        headerRow,
        el("div", { class: "grid-2" }, el("div", {}, el("label", {}, "Number"), ref),
          el("div", {}, el("label", {}, "Due date"), due)),
        el("div", { class: "hint" }, item.text.slice(0, 300)));
      return { item, ref, due, node: rowCard };
    });
    const save = el("button", { type: "button" }, "Save as alerts");
    save.addEventListener("click", async () => {
      const result = await api.saveAlerts(kind.value, rows.map((r) => ({
        ref: r.ref.value, text: r.item.text, due: r.due.value || null })));
      paste.value = ""; preview.replaceChildren();
      status.replaceChildren(notice("ok", `${result.added} saved.`));
      refresh();
    });
    preview.append(...rows.map((r) => r.node), save);
  });

  container.append(el("h1", {}, "Daily GeM check"),
    el("div", { class: "subtle" }, "Log in to GeM yourself, copy what is waiting for you, paste it here. I never log in."),
    form, el("h2", {}, "Waiting for you"), list);
  await refresh();
}
