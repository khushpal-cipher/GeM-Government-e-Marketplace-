import { el, notice } from "../dom.js";

// Step 1.5: Rejection reason reader + challenge draft.
// He pastes the buyer's disqualification reason from GeM (Bids -> List of Bids -> Already participated -> View Result).
// The app names the missing document, checks it against the profile, drafts the one-time challenge with the 48h deadline,
// and remembers the reason so future checklists warn earlier.

export async function renderRejections(container, _params, api) {
  const status = el("div");
  const resultCard = el("div");
  const historyList = el("div");

  async function refreshHistory() {
    try {
      const data = await api.getRejectionHistory();
      const items = data.items || [];
      if (!items.length) {
        historyList.replaceChildren(el("div", { class: "subtle" }, "No past rejections recorded yet."));
        return;
      }
      const cards = items.map((item) => {
        const delBtn = el("button", { type: "button", class: "secondary", style: "font-size:12px; padding:2px 8px;" }, "Delete");
        delBtn.addEventListener("click", async () => {
          if (confirm("Remove this rejection from history?")) {
            await api.deleteRejectionHistory(item.id);
            await refreshHistory();
          }
        });
        return el("div", { class: "card", style: "margin-bottom:8px;" },
          el("div", { class: "row" },
            el("strong", {}, item.bid_number || "Bid rejection"),
            item.missing_doc ? el("span", { class: "badge bad" }, item.missing_doc) : null,
            delBtn),
          el("div", { class: "hint", style: "margin-top:4px;" }, `Reason: "${item.reason_text}"`),
          el("div", { class: "hint" }, `Recorded: ${item.created_at ? item.created_at.slice(0, 10) : "recently"}`));
      });
      historyList.replaceChildren(...cards);
    } catch (err) {
      historyList.replaceChildren(notice("bad", `Error loading history: ${err.message}`));
    }
  }

  function displayAnalysis(analysis) {
    resultCard.replaceChildren();

    const header = el("div", { class: "row" },
      el("strong", { style: "font-size:16px;" }, `Analysis${analysis.bid_number ? `: ${analysis.bid_number}` : ""}`),
      el("span", { class: "badge bad" }, analysis.primary_reason),
      el("span", { class: "badge warn" }, analysis.deadline_text));

    const docsList = el("ul", { style: "margin: 6px 0 12px 20px; padding: 0;" },
      ...(analysis.missing_docs || []).map(d => el("li", { style: "margin-bottom: 6px;" },
        el("strong", {}, d.name),
        el("span", { class: `badge ${d.in_profile === true ? "ok" : (d.in_profile === false ? "bad" : "warn")}`, style: "margin-left: 6px;" },
          d.in_profile === true ? "In profile" : (d.in_profile === false ? "Missing from profile" : "Check manual")),
        el("div", { class: "hint" }, `${d.profile_note} (Quote: "${d.quote}")`))));

    const rebuttals = analysis.rebuttal_points && analysis.rebuttal_points.length
      ? el("div", { style: "margin: 8px 0;" },
          el("strong", {}, "Profile rebuttal grounds:"),
          el("ul", { style: "margin: 4px 0 10px 20px; padding: 0;" },
            ...analysis.rebuttal_points.map(r => el("li", { class: "hint", style: "margin-bottom: 4px;" }, r))))
      : null;

    const draftArea = el("textarea", {
      rows: "12",
      style: "width: 100%; font-family: monospace; font-size: 13px; margin-top: 6px;",
      readonly: "true",
    }, analysis.challenge_draft);

    const copyBtn = el("button", {
      type: "button",
      click: (e) => {
        navigator.clipboard.writeText(analysis.challenge_draft);
        e.target.textContent = "Copied!";
        setTimeout(() => { e.target.textContent = "Copy challenge draft"; }, 2000);
      }
    }, "Copy challenge draft");

    const saveBtn = el("button", {
      type: "button",
      class: "secondary",
      click: async (e) => {
        e.target.disabled = true;
        try {
          await api.saveRejectionHistory(
            analysis.bid_number,
            analysis.raw_text,
            analysis.primary_reason,
            analysis.primary_reason.toLowerCase()
          );
          e.target.textContent = "Saved to history";
          await refreshHistory();
        } catch (err) {
          e.target.disabled = false;
          alert("Error saving: " + err.message);
        }
      }
    }, "Remember this rejection");

    const box = el("div", { class: "card", style: "margin-top:16px; border: 1px solid #d1d5db;" },
      header,
      el("div", { class: "hint", style: "margin: 8px 0;" }, `Summary: ${analysis.summary}`),
      analysis.missing_docs && analysis.missing_docs.length ? el("div", {}, el("strong", {}, "Identified requirements:"), docsList) : null,
      rebuttals,
      el("label", { style: "margin-top:10px; display:block;" }, "One-time challenge representation draft (48h window):"),
      draftArea,
      el("div", { class: "row", style: "margin-top: 10px;" }, copyBtn, saveBtn));

    resultCard.replaceChildren(box);
  }

  // Form
  const pasteInput = el("textarea", {
    id: "rejection-paste",
    rows: "5",
    placeholder: "Example: Bid GEM/2026/B/8765432 disqualified in technical evaluation: Non-submission of OEM Authorisation certificate as per ATC clause 4.",
  });
  const bidNoInput = el("input", { type: "text", placeholder: "e.g. GEM/2026/B/8765432 (optional)" });
  const evalDateInput = el("input", { type: "date" });
  const submitBtn = el("button", { type: "submit" }, "Analyze & Draft Challenge");

  const form = el("form", { class: "card" },
    el("label", { for: "rejection-paste" }, "Paste buyer's disqualification reason:"),
    pasteInput,
    el("div", { class: "grid-2", style: "margin-top:8px;" },
      el("div", {}, el("label", {}, "Bid number (if not in paste)"), bidNoInput),
      el("div", {}, el("label", {}, "Date of technical evaluation"), evalDateInput)),
    el("div", { class: "hint", style: "margin-top:4px;" }, "Under GeM rules, you have 48 hours to challenge a technical rejection once. Stays local."),
    el("div", { class: "row", style: "margin-top:12px;" }, submitBtn),
    status,
    resultCard);

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    status.replaceChildren();
    resultCard.replaceChildren();
    const text = pasteInput.value.trim();
    if (!text) {
      status.replaceChildren(notice("bad", "Please paste the rejection text first."));
      return;
    }
    submitBtn.disabled = true;
    try {
      const analysis = await api.analyzeRejection(
        text,
        bidNoInput.value.trim() || null,
        evalDateInput.value || null
      );
      displayAnalysis(analysis);
    } catch (err) {
      status.replaceChildren(notice("bad", `Analysis failed: ${err.message}`));
    } finally {
      submitBtn.disabled = false;
    }
  });

  const historyCard = el("div", { class: "card", style: "margin-top:20px;" },
    el("div", { class: "row" },
      el("strong", { style: "font-size:16px;" }, "Past Rejections History"),
      el("span", { class: "hint" }, "Remembered so future bid checklists warn you earlier")),
    el("div", { style: "margin-top:10px;" }, historyList));

  container.append(
    el("h1", {}, "Rejection Reason Reader & Challenge Draft"),
    el("div", { class: "subtle" }, "Turn technical disqualifications into structured 48-hour challenges, and remember reasons to avoid repeating them."),
    form,
    historyCard
  );

  await refreshHistory();
}
