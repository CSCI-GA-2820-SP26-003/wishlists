(function () {
    const API_BASE_URL = "/api/wishlists";

    function getField(id) {
        return document.getElementById(id);
    }

    function flashMessage(message) {
        getField("flash_message").textContent = message;
    }

    function updateFormData(wishlist) {
        getField("wishlist_id").value = wishlist.id || "";
        getField("wishlist_name").value = wishlist.name || "";
        getField("wishlist_customer_id").value = wishlist.customer_id || "";
        getField("wishlist_description").value = wishlist.description || "";
        getField("wishlist_is_private").value = wishlist.is_private === true ? "true" : "false";
    }

    function createCell(row, value) {
        const cell = document.createElement("td");
        cell.textContent = value;
        row.appendChild(cell);
    }

    function renderResults(wishlists) {
        const body = getField("results_body");
        body.innerHTML = "";

        if (!wishlists.length) {
            const row = document.createElement("tr");
            row.className = "empty-row";
            const cell = document.createElement("td");
            cell.colSpan = 5;
            cell.textContent = "No wishlists found.";
            row.appendChild(cell);
            body.appendChild(row);
            return;
        }

        wishlists.forEach(function (wishlist) {
            const row = document.createElement("tr");
            createCell(row, wishlist.id);
            createCell(row, wishlist.name);
            createCell(row, wishlist.customer_id);
            createCell(row, wishlist.is_private === true ? "Private" : "Public");
            createCell(row, wishlist.description || "");
            body.appendChild(row);
        });
    }

    async function parseJsonResponse(response) {
        if (response.status === 204 || response.status === 205) {
            return null;
        }

        const contentType = response.headers.get("content-type") || "";
        if (!contentType.includes("application/json")) {
            return null;
        }

        const responseText = await response.text();
        if (!responseText.trim()) {
            return null;
        }

        return JSON.parse(responseText);
    }

    async function requestJson(url, options) {
        const response = await fetch(url, options);
        const data = await parseJsonResponse(response);

        if (!response.ok) {
            const message = data && data.message
                ? data.message
                : "Request failed with status " + response.status;
            throw new Error(message);
        }

        return data;
    }

    function parseCustomerId(rawValue, required) {
        const trimmed = rawValue.trim();
        if (!trimmed) {
            if (required) {
                throw new Error("Customer ID is required");
            }
            return null;
        }

        const parsed = Number.parseInt(trimmed, 10);
        if (Number.isNaN(parsed)) {
            throw new Error("Customer ID must be an integer");
        }

        return parsed;
    }

    function parseWishlistId(rawValue) {
        const trimmed = rawValue.trim();
        if (!trimmed) {
            throw new Error("Wishlist ID is required");
        }

        if (!/^\d+$/.test(trimmed)) {
            throw new Error("Wishlist ID must be an integer");
        }

        const parsed = Number.parseInt(trimmed, 10);
        if (Number.isNaN(parsed)) {
            throw new Error("Wishlist ID must be an integer");
        }

        return parsed;
    }

    function collectCreatePayload() {
        const name = getField("wishlist_name").value.trim();
        const description = getField("wishlist_description").value.trim();
        const customerId = parseCustomerId(getField("wishlist_customer_id").value, true);

        if (!name) {
            throw new Error("Name is required");
        }

        return {
            name: name,
            customer_id: customerId,
            description: description || null
        };
    }

    function collectUpdatePayload() {
        const name = getField("wishlist_name").value.trim();
        const description = getField("wishlist_description").value.trim();

        if (!name) {
            throw new Error("Name is required");
        }

        return {
            name: name,
            description: description
        };
    }

    function buildSearchQuery() {
        const params = new URLSearchParams();
        const name = getField("wishlist_name").value.trim();
        const description = getField("wishlist_description").value.trim();
        const customerId = parseCustomerId(getField("wishlist_customer_id").value, false);

        if (customerId !== null) {
            params.set("customer_id", customerId);
        }
        if (name) {
            params.set("name", name);
        }
        if (description) {
            params.set("description", description);
        }

        const query = params.toString();
        return query ? "?" + query : "";
    }

    async function createWishlist() {
        try {
            const wishlist = await requestJson(API_BASE_URL, {
                method: "POST",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(collectCreatePayload())
            });

            updateFormData(wishlist);
            renderResults([wishlist]);
            flashMessage("Success");
        } catch (error) {
            flashMessage(error.message);
        }
    }

    async function searchWishlists() {
        try {
            const wishlists = await requestJson(API_BASE_URL + buildSearchQuery(), {
                method: "GET",
                headers: {
                    "Accept": "application/json"
                }
            });

            renderResults(wishlists);
            if (wishlists.length > 0) {
                updateFormData(wishlists[0]);
            }
            flashMessage("Success");
        } catch (error) {
            flashMessage(error.message);
        }
    }

    async function retrieveWishlist() {
        try {
            const wishlistId = parseWishlistId(getField("wishlist_id").value);
            const wishlist = await requestJson(API_BASE_URL + "/" + wishlistId, {
                method: "GET",
                headers: {
                    "Accept": "application/json"
                }
            });

            updateFormData(wishlist);
            renderResults([wishlist]);
            flashMessage("Success");
        } catch (error) {
            flashMessage(error.message);
        }
    }

    async function updateWishlist() {
        try {
            const wishlistId = parseWishlistId(getField("wishlist_id").value);
            const wishlist = await requestJson(API_BASE_URL + "/" + wishlistId, {
                method: "PUT",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(collectUpdatePayload())
            });

            updateFormData(wishlist);
            renderResults([wishlist]);
            flashMessage("Success");
        } catch (error) {
            flashMessage(error.message);
        }
    }

    async function makeWishlistPrivate() {
        try {
            const wishlistId = parseWishlistId(getField("wishlist_id").value);
            await requestJson(API_BASE_URL + "/" + wishlistId + "/private", {
                method: "POST",
                headers: {
                    "Accept": "application/json"
                }
            });

            const wishlist = await requestJson(API_BASE_URL + "/" + wishlistId, {
                method: "GET",
                headers: {
                    "Accept": "application/json"
                }
            });

            updateFormData(wishlist);
            renderResults([wishlist]);
            flashMessage("Success");
        } catch (error) {
            flashMessage(error.message);
        }
    }

    async function deleteWishlist() {
        try {
            const wishlistId = parseWishlistId(getField("wishlist_id").value);
            await requestJson(API_BASE_URL + "/" + wishlistId, {
                method: "DELETE",
                headers: {
                    "Accept": "application/json"
                }
            });

            renderResults([]);
            updateFormData({});
            flashMessage("Success");
        } catch (error) {
            flashMessage(error.message);
        }
    }

    getField("create-btn").addEventListener("click", createWishlist);
    getField("update-btn").addEventListener("click", updateWishlist);
    getField("retrieve-btn").addEventListener("click", retrieveWishlist);
    getField("make_private-btn").addEventListener("click", makeWishlistPrivate);
    getField("delete-btn").addEventListener("click", deleteWishlist);
    getField("search-btn").addEventListener("click", searchWishlists);
})();
