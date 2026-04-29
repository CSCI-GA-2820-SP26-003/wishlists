"""
HTML for the /demo page used in the sprint review.
"""


def get_demo_html() -> str:
    return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Wishlist Service - Final Demo</title>
  <style>
    :root {
      --bg: #f3f6fb;
      --text: #102039;
      --muted: #5f6b80;
      --card: #ffffff;
      --line: #d8e1f0;
      --primary: #2f6fed;
      --primary-dark: #2059c6;
      --secondary: #e7edf8;
      --secondary-dark: #d7e1f4;
      --shadow: 0 10px 28px rgba(18, 32, 57, 0.08);
    }
    * { box-sizing: border-box; }
    body {
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      margin: 0;
      padding: 24px;
      line-height: 1.4;
      background: linear-gradient(180deg, #f8fbff 0%, var(--bg) 100%);
      color: var(--text);
    }
    h1 {
      font-size: 1.8rem;
      margin: 0 0 0.4rem;
      letter-spacing: -0.02em;
    }
    h2 {
      font-size: 1.15rem;
      margin: 0 0 0.8rem;
      color: #0f2b59;
    }
    section {
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 14px 16px;
      margin-bottom: 14px;
      box-shadow: var(--shadow);
    }
    label {
      display: block;
      margin-top: 6px;
      font-size: 0.82rem;
      font-weight: 600;
      color: #32496d;
      text-transform: uppercase;
      letter-spacing: 0.02em;
    }
    input {
      padding: 7px 9px;
      margin-top: 3px;
      font-size: 0.92rem;
      width: 230px;
      border: 1px solid #c8d5ea;
      border-radius: 8px;
      background: #fcfdff;
      color: var(--text);
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }
    input:focus {
      outline: none;
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(47, 111, 237, 0.16);
    }
    button {
      margin-top: 8px;
      margin-right: 4px;
      padding: 7px 12px;
      font-size: 0.9rem;
      cursor: pointer;
      border-radius: 8px;
      border: none;
      transition: transform 0.04s ease, filter 0.15s ease, background 0.15s ease;
    }
    button:hover { filter: brightness(0.98); }
    button:active { transform: translateY(1px); }
    button.primary {
      background: var(--primary);
      color: white;
      box-shadow: 0 6px 14px rgba(47, 111, 237, 0.28);
    }
    button.primary:hover { background: var(--primary-dark); }
    button.secondary {
      background: var(--secondary);
      color: #1f3356;
      border: 1px solid #cfdbf2;
    }
    button.secondary:hover { background: var(--secondary-dark); }
    .row {
      display: flex;
      flex-wrap: wrap;
      gap: 10px 24px;
      align-items: flex-end;
    }
    pre {
      background: #0b1020;
      color: #e5e7eb;
      padding: 12px;
      border-radius: 10px;
      border: 1px solid #1e2940;
      font-size: 0.8rem;
      max-height: 320px;
      overflow: auto;
    }
    code {
      font-family: SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    }
    .small {
      font-size: 0.88rem;
      color: var(--muted);
      margin: 0.15rem 0 0.45rem;
    }
    #current-wishlist-label {
      color: #0b5ed7;
      background: #e9f2ff;
      border: 1px solid #c8dcff;
      padding: 2px 8px;
      border-radius: 999px;
      font-size: 0.86rem;
    }
    @media (max-width: 760px) {
      body { padding: 14px; }
      input { width: 100%; min-width: 180px; }
      .row > div { min-width: 100%; }
    }
  </style>
</head>
<body>
  <h1>Wishlist Service - Final Demo</h1>
  <p class="small">
    This page calls the same REST API you built in Sprint 1. Use it to quickly demo Create, Read, Update, Delete, and List.
  </p>
  <p class="small">
    Current wishlist: <strong><span id="current-wishlist-label">None selected</span></strong>
  </p>

  <section>
    <h2>1. Create and list wishlists</h2>
    <div class="row">
      <div>
        <label for="w-name">Name</label>
        <input id="w-name" type="text" placeholder="e.g., Birthday Gifts" />
      </div>
      <div>
        <label for="w-customer">Customer ID</label>
        <input id="w-customer" type="number" placeholder="e.g., 123" />
      </div>
      <div>
        <label for="w-desc">Description</label>
        <input id="w-desc" type="text" placeholder="Optional description" />
      </div>
      <div>
        <button class="primary" onclick="createWishlist()">Create Wishlist</button>
      </div>
    </div>
    <div style="margin-top: 10px;">
      <button class="secondary" onclick="listWishlists()">List All Wishlists</button>
    </div>
  </section>

  <section>
    <h2>2. View a wishlist and its items</h2>
    <div class="row">
      <div>
        <label for="view-wishlist-id">Wishlist ID</label>
        <input id="view-wishlist-id" type="number" placeholder="Wishlist ID" />
      </div>
      <div>
        <button class="secondary" onclick="getWishlist()">Get Wishlist</button>
      </div>
    </div>
  </section>

  <section>
    <h2>3. Add an item to a wishlist</h2>
    <div class="row">
      <div>
        <label for="item-wishlist-id">Wishlist ID</label>
        <input id="item-wishlist-id" type="number" placeholder="Wishlist ID" />
      </div>
      <div>
        <label for="item-product-id">Product ID</label>
        <input id="item-product-id" type="text" placeholder="e.g., SKU-001" />
      </div>
      <div>
        <label for="item-product-name">Product Name</label>
        <input id="item-product-name" type="text" placeholder="e.g., Sneakers" />
      </div>
      <div>
        <label for="item-variant-id">Variant ID</label>
        <input id="item-variant-id" type="text" placeholder="e.g., VAR-001" />
      </div>
      <div>
        <label for="item-quantity">Quantity</label>
        <input id="item-quantity" type="number" value="1" />
      </div>
      <div>
        <button class="primary" onclick="addItem()">Add Item</button>
      </div>
    </div>
    <div style="margin-top: 10px;">
      <div class="row">
        <div>
          <label for="list-items-wishlist-id">Wishlist ID</label>
          <input id="list-items-wishlist-id" type="number" placeholder="Wishlist ID" />
        </div>
        <div>
          <button class="secondary" onclick="listItems()">List Items</button>
        </div>
      </div>
    </div>
  </section>

  <section>
    <h2>4. Update and delete</h2>
    <div class="row">
      <div>
        <label for="update-wishlist-id">Wishlist ID</label>
        <input id="update-wishlist-id" type="number" placeholder="Wishlist ID" />
      </div>
      <div>
        <label for="update-name">New Name</label>
        <input id="update-name" type="text" placeholder="New wishlist name" />
      </div>
      <div>
        <label for="update-desc">New Description</label>
        <input id="update-desc" type="text" placeholder="New description" />
      </div>
      <div>
        <button class="secondary" onclick="updateWishlist()">Update Wishlist</button>
      </div>
    </div>
    <div style="margin-top: 12px;" class="row">
      <div>
        <label for="delete-wishlist-id">Wishlist ID</label>
        <input id="delete-wishlist-id" type="number" placeholder="Wishlist ID" />
      </div>
      <div>
        <button class="secondary" onclick="deleteWishlist()">Delete Wishlist</button>
      </div>
    </div>
    <div style="margin-top: 12px;" class="row">
      <div>
        <label for="delete-item-wishlist-id">Wishlist ID</label>
        <input id="delete-item-wishlist-id" type="number" placeholder="Wishlist ID" />
      </div>
      <div>
        <label for="delete-item-id">Item ID</label>
        <input id="delete-item-id" type="number" placeholder="Item ID" />
      </div>
      <div>
        <button class="secondary" onclick="deleteItem()">Delete Item</button>
      </div>
    </div>
  </section>

  <section>
    <h2>5. Last request / response</h2>
    <p class="small">
      This shows the raw HTTP call that was made and the JSON response. You can use this in the sprint review to talk about status codes and sad paths.
    </p>
    <pre id="log"><code>Ready.</code></pre>
  </section>

  <script>
    const baseUrl = "/wishlists";
    let currentWishlistId = null;

    function setCurrentWishlist(id) {
      currentWishlistId = id;
      const label = document.getElementById("current-wishlist-label");
      if (label) {
        label.textContent = id != null ? String(id) : "None selected";
      }
      const fieldIds = [
        "view-wishlist-id",
        "item-wishlist-id",
        "list-items-wishlist-id",
        "update-wishlist-id",
        "delete-wishlist-id",
        "delete-item-wishlist-id",
      ];
      fieldIds.forEach((fid) => {
        const el = document.getElementById(fid);
        if (el) {
          el.value = id != null ? String(id) : "";
        }
      });
    }

    function logResult(method, url, status, data, body) {
      const panel = document.getElementById("log");
      const formatted = JSON.stringify(data, null, 2);
      const bodyText = body ? JSON.stringify(body, null, 2) : "";
      panel.textContent =
        method + " " + url + "\\n" +
        "Status: " + status + "\\n" +
        (body ? "\\nRequest body:\\n" + bodyText + "\\n" : "") +
        "\\nResponse body:\\n" + formatted;
    }

    function fallbackUrl(url, useFallback) {
      if (!useFallback) return url;
      return url.startsWith("/api/") ? url.replace("/api/", "/") : url;
    }

    async function readJsonOrText(resp) {
      const text = await resp.text();
      if (!text) {
        return {};
      }
      try {
        return JSON.parse(text);
      } catch (e) {
        return { raw: text };
      }
    }

    function logClientError(message) {
      const panel = document.getElementById("log");
      panel.textContent = "Client validation error:\\n" + message;
    }

    async function apiFetch(url, options) {
      let resp = await fetch(url, options);
      if (resp.status !== 404) {
        return { resp: resp, usedUrl: url };
      }
      const altUrl = fallbackUrl(url, true);
      if (altUrl === url) {
        return { resp: resp, usedUrl: url };
      }
      resp = await fetch(altUrl, options);
      return { resp: resp, usedUrl: altUrl };
    }

    async function createWishlist() {
      const name = document.getElementById("w-name").value;
      const customer = document.getElementById("w-customer").value;
      const desc = document.getElementById("w-desc").value;
      const payload = {
        name: name,
        customer_id: customer ? Number(customer) : undefined,
        description: desc || undefined,
      };
      const body = JSON.parse(JSON.stringify(payload));
      const result = await apiFetch(baseUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await readJsonOrText(result.resp);
      logResult("POST", result.usedUrl, result.resp.status, data, body);
      if (result.resp.ok && data && typeof data.id !== "undefined") {
        setCurrentWishlist(data.id);
      }
    }

    async function listWishlists() {
      const result = await apiFetch(baseUrl);
      const data = await readJsonOrText(result.resp);
      logResult("GET", result.usedUrl, result.resp.status, data);
    }

    async function getWishlist() {
      const rawId = document.getElementById("view-wishlist-id").value;
      const id = rawId || currentWishlistId;
      if (!id) {
        logClientError("Wishlist ID is required for Get Wishlist.");
        return;
      }
      const url = baseUrl + "/" + String(id);
      const result = await apiFetch(url);
      const data = await readJsonOrText(result.resp);
      logResult("GET", result.usedUrl, result.resp.status, data);
      if (result.resp.ok && data && typeof data.id !== "undefined") {
        setCurrentWishlist(data.id);
      }
    }

    async function addItem() {
      const rawId = document.getElementById("item-wishlist-id").value;
      const wId = rawId || currentWishlistId;
      if (!wId) {
        logClientError("Wishlist ID is required for Add Item.");
        return;
      }
      const url = baseUrl + "/" + String(wId) + "/items";
      const payload = {
        product_id: document.getElementById("item-product-id").value,
        product_name: document.getElementById("item-product-name").value,
        variant_id: document.getElementById("item-variant-id").value,
        quantity: Number(document.getElementById("item-quantity").value || "1"),
      };
      if (!payload.product_id || !payload.product_name || !payload.variant_id) {
        logClientError("Product ID, Product Name, and Variant ID are required for Add Item.");
        return;
      }
      const body = JSON.parse(JSON.stringify(payload));
      const result = await apiFetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await readJsonOrText(result.resp);
      logResult("POST", result.usedUrl, result.resp.status, data, body);
    }

    async function listItems() {
      const rawId = document.getElementById("list-items-wishlist-id").value;
      const wId = rawId || currentWishlistId;
      if (!wId) {
        logClientError("Wishlist ID is required for List Items.");
        return;
      }
      const url = baseUrl + "/" + String(wId) + "/items";
      const result = await apiFetch(url);
      const data = await readJsonOrText(result.resp);
      logResult("GET", result.usedUrl, result.resp.status, data);
    }

    async function updateWishlist() {
      const rawId = document.getElementById("update-wishlist-id").value;
      const id = rawId || currentWishlistId;
      if (!id) {
        logClientError("Wishlist ID is required for Update Wishlist.");
        return;
      }
      const url = baseUrl + "/" + String(id);
      const payload = {
        name: document.getElementById("update-name").value,
        description: document.getElementById("update-desc").value,
      };
      if (!payload.name || !payload.name.trim()) {
        logClientError("Name is required for Update Wishlist.");
        return;
      }
      const body = JSON.parse(JSON.stringify(payload));
      const result = await apiFetch(url, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await readJsonOrText(result.resp);
      logResult("PUT", result.usedUrl, result.resp.status, data, body);
      if (result.resp.ok && data && typeof data.id !== "undefined") {
        setCurrentWishlist(data.id);
      }
    }

    async function deleteWishlist() {
      const rawId = document.getElementById("delete-wishlist-id").value;
      const id = rawId || currentWishlistId;
      if (!id) {
        logClientError("Wishlist ID is required for Delete Wishlist.");
        return;
      }
      const url = baseUrl + "/" + String(id);
      const result = await apiFetch(url, { method: "DELETE" });
      const data = await readJsonOrText(result.resp);
      logResult("DELETE", result.usedUrl, result.resp.status, data);
    }

    async function deleteItem() {
      const rawId = document.getElementById("delete-item-wishlist-id").value;
      const wId = rawId || currentWishlistId;
      const itemId = document.getElementById("delete-item-id").value;
      if (!wId || !itemId) {
        logClientError("Wishlist ID and Item ID are required for Delete Item.");
        return;
      }
      const url = baseUrl + "/" + String(wId) + "/items/" + String(itemId);
      const result = await apiFetch(url, { method: "DELETE" });
      const data = await readJsonOrText(result.resp);
      logResult("DELETE", result.usedUrl, result.resp.status, data);
    }
  </script>
</body>
</html>
"""
"""
HTML for the /demo page used in the sprint review.
"""


def get_demo_html() -> str:
    return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Wishlist Service – Final Demo</title>
  <style>
    :root {
      --bg: #f3f6fb;
      --text: #102039;
      --muted: #5f6b80;
      --card: #ffffff;
      --line: #d8e1f0;
      --primary: #2f6fed;
      --primary-dark: #2059c6;
      --secondary: #e7edf8;
      --secondary-dark: #d7e1f4;
      --shadow: 0 10px 28px rgba(18, 32, 57, 0.08);
    }
    * { box-sizing: border-box; }
    body {
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      margin: 0;
      padding: 24px;
      line-height: 1.4;
      background: linear-gradient(180deg, #f8fbff 0%, var(--bg) 100%);
      color: var(--text);
    }
    h1 {
      font-size: 1.8rem;
      margin: 0 0 0.4rem;
      letter-spacing: -0.02em;
    }
    h2 {
      font-size: 1.15rem;
      margin: 0 0 0.8rem;
      color: #0f2b59;
    }
    section {
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 14px 16px;
      margin-bottom: 14px;
      box-shadow: var(--shadow);
    }
    label {
      display: block;
      margin-top: 6px;
      font-size: 0.82rem;
      font-weight: 600;
      color: #32496d;
      text-transform: uppercase;
      letter-spacing: 0.02em;
    }
    input {
      padding: 7px 9px;
      margin-top: 3px;
      font-size: 0.92rem;
      width: 230px;
      border: 1px solid #c8d5ea;
      border-radius: 8px;
      background: #fcfdff;
      color: var(--text);
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }
    input:focus {
      outline: none;
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(47, 111, 237, 0.16);
    }
    button {
      margin-top: 8px;
      margin-right: 4px;
      padding: 7px 12px;
      font-size: 0.9rem;
      cursor: pointer;
      border-radius: 8px;
      border: none;
      transition: transform 0.04s ease, filter 0.15s ease, background 0.15s ease;
    }
    button:hover { filter: brightness(0.98); }
    button:active { transform: translateY(1px); }
    button.primary {
      background: var(--primary);
      color: white;
      box-shadow: 0 6px 14px rgba(47, 111, 237, 0.28);
    }
    button.primary:hover { background: var(--primary-dark); }
    button.secondary {
      background: var(--secondary);
      color: #1f3356;
      border: 1px solid #cfdbf2;
    }
    button.secondary:hover { background: var(--secondary-dark); }
    .row {
      display: flex;
      flex-wrap: wrap;
      gap: 10px 24px;
      align-items: flex-end;
    }
    pre {
      background: #0b1020;
      color: #e5e7eb;
      padding: 12px;
      border-radius: 10px;
      border: 1px solid #1e2940;
      font-size: 0.8rem;
      max-height: 320px;
      overflow: auto;
    }
    code {
      font-family: SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    }
    .small {
      font-size: 0.88rem;
      color: var(--muted);
      margin: 0.15rem 0 0.45rem;
    }
    #current-wishlist-label {
      color: #0b5ed7;
      background: #e9f2ff;
      border: 1px solid #c8dcff;
      padding: 2px 8px;
      border-radius: 999px;
      font-size: 0.86rem;
    }
    @media (max-width: 760px) {
      body { padding: 14px; }
      input { width: 100%; min-width: 180px; }
      .row > div { min-width: 100%; }
    }
  </style>
</head>
<body>
  <h1>Wishlist Service – Final Demo</h1>
  <p class="small">
    This page calls the same REST API you built in Sprint 1. Use it to quickly demo Create, Read, Update, Delete, and List.
  </p>
  <p class="small">
    Current wishlist: <strong><span id="current-wishlist-label">None selected</span></strong>
  </p>

  <section>
    <h2>1. Create and list wishlists</h2>
    <div class="row">
      <div>
        <label for="w-name">Name</label>
        <input id="w-name" type="text" placeholder="e.g., Birthday Gifts" />
      </div>
      <div>
        <label for="w-customer">Customer ID</label>
        <input id="w-customer" type="number" placeholder="e.g., 123" />
      </div>
      <div>
        <label for="w-desc">Description</label>
        <input id="w-desc" type="text" placeholder="Optional description" />
      </div>
      <div>
        <button class="primary" onclick="createWishlist()">Create Wishlist</button>
      </div>
    </div>
    <div style="margin-top: 10px;">
      <button class="secondary" onclick="listWishlists()">List All Wishlists</button>
    </div>
  </section>

  <section>
    <h2>2. View a wishlist and its items</h2>
    <div class="row">
      <div>
        <label for="view-wishlist-id">Wishlist ID</label>
        <input id="view-wishlist-id" type="number" placeholder="Wishlist ID" />
      </div>
      <div>
        <button class="secondary" onclick="getWishlist()">Get Wishlist</button>
      </div>
    </div>
  </section>

  <section>
    <h2>3. Add an item to a wishlist</h2>
    <div class="row">
      <div>
        <label for="item-wishlist-id">Wishlist ID</label>
        <input id="item-wishlist-id" type="number" placeholder="Wishlist ID" />
      </div>
      <div>
        <label for="item-product-id">Product ID</label>
        <input id="item-product-id" type="text" placeholder="e.g., SKU-001" />
      </div>
      <div>
        <label for="item-product-name">Product Name</label>
        <input id="item-product-name" type="text" placeholder="e.g., Sneakers" />
      </div>
      <div>
        <label for="item-variant-id">Variant ID</label>
        <input id="item-variant-id" type="text" placeholder="e.g., VAR-001" />
      </div>
      <div>
        <label for="item-quantity">Quantity</label>
        <input id="item-quantity" type="number" value="1" />
      </div>
      <div>
        <button class="primary" onclick="addItem()">Add Item</button>
      </div>
    </div>
    <div style="margin-top: 10px;">
      <div class="row">
        <div>
          <label for="list-items-wishlist-id">Wishlist ID</label>
          <input id="list-items-wishlist-id" type="number" placeholder="Wishlist ID" />
        </div>
        <div>
          <button class="secondary" onclick="listItems()">List Items</button>
        </div>
      </div>
    </div>
  </section>

  <section>
    <h2>4. Update and delete</h2>
    <div class="row">
      <div>
        <label for="update-wishlist-id">Wishlist ID</label>
        <input id="update-wishlist-id" type="number" placeholder="Wishlist ID" />
      </div>
      <div>
        <label for="update-name">New Name</label>
        <input id="update-name" type="text" placeholder="New wishlist name" />
      </div>
      <div>
        <label for="update-desc">New Description</label>
        <input id="update-desc" type="text" placeholder="New description" />
      </div>
      <div>
        <button class="secondary" onclick="updateWishlist()">Update Wishlist</button>
      </div>
    </div>
    <div style="margin-top: 12px;" class="row">
      <div>
        <label for="delete-wishlist-id">Wishlist ID</label>
        <input id="delete-wishlist-id" type="number" placeholder="Wishlist ID" />
      </div>
      <div>
        <button class="secondary" onclick="deleteWishlist()">Delete Wishlist</button>
      </div>
    </div>
    <div style="margin-top: 12px;" class="row">
      <div>
        <label for="delete-item-wishlist-id">Wishlist ID</label>
        <input id="delete-item-wishlist-id" type="number" placeholder="Wishlist ID" />
      </div>
      <div>
        <label for="delete-item-id">Item ID</label>
        <input id="delete-item-id" type="number" placeholder="Item ID" />
      </div>
      <div>
        <button class="secondary" onclick="deleteItem()">Delete Item</button>
      </div>
    </div>
  </section>

  <section>
    <h2>5. Last request / response</h2>
    <p class="small">
      This shows the raw HTTP call that was made and the JSON response. You can use this in the sprint review to talk about status codes and sad paths.
    </p>
    <pre id="log"><code>Ready.</code></pre>
  </section>

  <script>
    const baseUrl = "/wishlists";
    let currentWishlistId = null;

    function setCurrentWishlist(id) {
      currentWishlistId = id;
      const label = document.getElementById("current-wishlist-label");
      if (label) {
        label.textContent = id != null ? String(id) : "None selected";
      }
      const fieldIds = [
        "view-wishlist-id",
        "item-wishlist-id",
        "list-items-wishlist-id",
        "update-wishlist-id",
        "delete-wishlist-id",
        "delete-item-wishlist-id",
      ];
      fieldIds.forEach((fid) => {
        const el = document.getElementById(fid);
        if (el) {
          el.value = id != null ? String(id) : "";
        }
      });
    }

    function logResult(method, url, status, data, body) {
      const panel = document.getElementById("log");
      const formatted = JSON.stringify(data, null, 2);
      const bodyText = body ? JSON.stringify(body, null, 2) : "";
      panel.textContent =
        method + " " + url + "\\n" +
        "Status: " + status + "\\n" +
        (body ? "\\nRequest body:\\n" + bodyText + "\\n" : "") +
        "\\nResponse body:\\n" + formatted;
    }

    async function createWishlist() {
      const name = document.getElementById("w-name").value;
      const customer = document.getElementById("w-customer").value;
      const desc = document.getElementById("w-desc").value;
      const payload = {
        name: name,
        customer_id: customer ? Number(customer) : undefined,
        description: desc || undefined,
      };
      const body = JSON.parse(JSON.stringify(payload));
      const resp = await fetch(baseUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await resp.json();
      logResult("POST", baseUrl, resp.status, data, body);
      if (resp.ok && data && typeof data.id !== "undefined") {
        setCurrentWishlist(data.id);
      }
    }

    async function listWishlists() {
      const resp = await fetch(baseUrl);
      const data = await resp.json();
      logResult("GET", baseUrl, resp.status, data);
    }

    async function getWishlist() {
      const rawId = document.getElementById("view-wishlist-id").value;
      const id = rawId || currentWishlistId;
      if (!id) return;
      const url = baseUrl + "/" + String(id);
      const resp = await fetch(url);
      const data = await resp.json();
      logResult("GET", url, resp.status, data);
      if (resp.ok && data && typeof data.id !== "undefined") {
        setCurrentWishlist(data.id);
      }
    }

    async function addItem() {
      const rawId = document.getElementById("item-wishlist-id").value;
      const wId = rawId || currentWishlistId;
      if (!wId) return;
      const url = baseUrl + "/" + String(wId) + "/items";
      const payload = {
        product_id: document.getElementById("item-product-id").value,
        product_name: document.getElementById("item-product-name").value,
        variant_id: document.getElementById("item-variant-id").value,
        quantity: Number(document.getElementById("item-quantity").value || "1"),
      };
      const body = JSON.parse(JSON.stringify(payload));
      const resp = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await resp.json();
      logResult("POST", url, resp.status, data, body);
    }

    async function listItems() {
      const rawId = document.getElementById("list-items-wishlist-id").value;
      const wId = rawId || currentWishlistId;
      if (!wId) return;
      const url = baseUrl + "/" + String(wId) + "/items";
      const resp = await fetch(url);
      const data = await resp.json();
      logResult("GET", url, resp.status, data);
    }

    async function updateWishlist() {
      const rawId = document.getElementById("update-wishlist-id").value;
      const id = rawId || currentWishlistId;
      if (!id) return;
      const url = baseUrl + "/" + String(id);
      const payload = {
        name: document.getElementById("update-name").value,
        description: document.getElementById("update-desc").value,
      };
      const body = JSON.parse(JSON.stringify(payload));
      const resp = await fetch(url, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await resp.json();
      logResult("PUT", url, resp.status, data, body);
      if (resp.ok && data && typeof data.id !== "undefined") {
        setCurrentWishlist(data.id);
      }
    }

    async function deleteWishlist() {
      const rawId = document.getElementById("delete-wishlist-id").value;
      const id = rawId || currentWishlistId;
      if (!id) return;
      const url = baseUrl + "/" + String(id);
      const resp = await fetch(url, { method: "DELETE" });
      let data = {};
      try {
        data = await resp.json();
      } catch (e) {
        data = {};
      }
      logResult("DELETE", url, resp.status, data);
    }

    async function deleteItem() {
      const rawId = document.getElementById("delete-item-wishlist-id").value;
      const wId = rawId || currentWishlistId;
      const itemId = document.getElementById("delete-item-id").value;
      if (!wId || !itemId) return;
      const url = baseUrl + "/" + String(wId) + "/items/" + String(itemId);
      const resp = await fetch(url, { method: "DELETE" });
      let data = {};
      try {
        data = await resp.json();
      } catch (e) {
        data = {};
      }
      logResult("DELETE", url, resp.status, data);
    }
  </script>
</body>
</html>
"""

