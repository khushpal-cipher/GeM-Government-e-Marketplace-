// The only module that talks HTTP. Views depend on this interface,
// not on fetch() or URLs, so the backend can change without touching views.

export class ApiError extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
  }
}

export class ApiClient {
  constructor(baseUrl = "/api") {
    this.baseUrl = baseUrl;
  }

  async #request(path, options = {}) {
    const response = await fetch(this.baseUrl + path, options);
    const isJson = (response.headers.get("content-type") || "").includes("application/json");
    const body = isJson ? await response.json() : null;
    if (!response.ok) {
      const detail = body && body.detail ? body.detail : response.statusText;
      throw new ApiError(response.status, typeof detail === "string" ? detail : JSON.stringify(detail));
    }
    return body;
  }

  #json(method, path, data) {
    return this.#request(path, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
  }

  // ---- bids ----
  listBids() { return this.#request("/bids"); }
  getBid(id) { return this.#request(`/bids/${encodeURIComponent(id)}`); }
  importBidPdf(file) {
    const form = new FormData();
    form.append("file", file);
    return this.#request("/bids/import", { method: "POST", body: form });
  }

  fetchBidByLink(link) { return this.#json("POST", "/bids/fetch", { link }); }

  // ---- discovery ----
  getDiscovery() { return this.#request("/discovery"); }
  runDiscovery() { return this.#request("/discovery/run", { method: "POST" }); }

  // ---- seller profile ----
  getProfile() { return this.#request("/profile"); }
  getAlertKinds() { return this.#request("/alerts/kinds"); }
  previewAlerts(kind, text) { return this.#json("POST", "/alerts/preview", { kind, text }); }
  saveAlerts(kind, items) { return this.#json("POST", "/alerts", { kind, items }); }
  getAlerts() { return this.#request("/alerts"); }
  finishAlert(id) { return this.#request(`/alerts/${id}/done`, { method: "POST" }); }
  getProfileWarnings() { return this.#request("/profile/warnings"); }
  saveProfile(profile) { return this.#json("PUT", "/profile", profile); }
  getShortfallReply(text, bidNumber = null, due = null) {
    return this.#json("POST", "/shortfall/reply", { text, bid_number: bidNumber, due });
  }

  // ---- order tracker ----
  getOrders() { return this.#request("/orders"); }
  getOrder(id) { return this.#request(`/orders/${encodeURIComponent(id)}`); }
  saveOrder(order) { return this.#json("POST", "/orders", order); }
  updateOrder(id, updates) { return this.#json("PUT", `/orders/${encodeURIComponent(id)}`, updates); }
  getOrderIncidentDraft(id) { return this.#request(`/orders/${encodeURIComponent(id)}/incident-draft`); }
  parseOrderPaste(text) { return this.#json("POST", "/orders/parse", { text }); }

  // ---- rejection & challenge ----
  analyzeRejection(text, bidNumber = null, evalDate = null) {
    return this.#json("POST", "/rejection/analyze", { text, bid_number: bidNumber, eval_date: evalDate });
  }
  saveRejectionHistory(bidNumber, reasonText, missingDoc, category = null) {
    return this.#json("POST", "/rejection/history", { bid_number: bidNumber, reason_text: reasonText, missing_doc: missingDoc, category });
  }
  getRejectionHistory() { return this.#request("/rejection/history"); }
  deleteRejectionHistory(id) { return this.#request(`/rejection/history/${id}`, { method: "DELETE" }); }
  getRejectionWarnings(docs) { return this.#request(`/rejection/warnings?docs=${encodeURIComponent(docs)}`); }

  // ---- login (website mode) ----
  getSession() { return this.#request("/session"); }
  login(password) { return this.#json("POST", "/login", { password }); }
  logout() { return this.#request("/logout", { method: "POST" }); }

  // ---- chat ----
  chatStatus() { return this.#request("/chat"); }
  chat(messages) { return this.#json("POST", "/chat", { messages }); }

  // ---- safety ----
  getSafety() { return this.#request("/safety"); }
  setContactEmail(email) { return this.#json("PUT", "/safety/contact", { email }); }
  resetBreaker(note) { return this.#json("POST", "/safety/reset", { confirmed: true, note }); }
}
