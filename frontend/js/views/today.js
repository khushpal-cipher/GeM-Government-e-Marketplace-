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

  function alertCard(a) {
    const done = el("button", { type: "button", class: "secondary" }, "Done");
    done.addEventListener("click", async () => { await api.finishAlert(a.id); refresh(); });
    return el("div", { class: "card" },
      el("div", { class: "row" },
        el("strong", {}, `${a.label}${a.ref ? `: ${a.ref}` : ""}`),
        el("span", { class: `badge ${a.overdue ? "bad" : "warn"}` }, a.due_text), done),
      el("div", { class: "hint" }, `Do it on GeM: ${a.where}`),
      el("div", { class: "hint" }, `If missed: ${a.if_missed}`),
      a.text ? el("div", { class: "hint" }, a.text.slice(0, 300)) : null);
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
      return { item, ref, due, node: el("div", { class: "card" },
        item.unclear ? notice("warn", `Please check: ${item.unclear}.`) : null,
        el("div", { class: "grid-2" }, el("div", {}, el("label", {}, "Number"), ref),
          el("div", {}, el("label", {}, "Due date"), due)),
        el("div", { class: "hint" }, item.text.slice(0, 300))) };
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
