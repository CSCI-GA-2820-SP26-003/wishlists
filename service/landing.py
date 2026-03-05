"""
HTML for the root landing page (GET /).
"""


def get_landing_html() -> str:
    """Return HTML for the root landing page (GET /)."""
    return """<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Wishlist Service</title></head>
<body style="font-family: system-ui, sans-serif; margin: 2rem; line-height: 1.5;">
  <h1>Wishlist Service is Up</h1>
  <p><strong>Wishlist REST API Service</strong> v1.0.</p>
  <p>These are the routes we serve:</p>
  <h2>Wishlists</h2>
  <table border="1" cellpadding="8" cellspacing="0">
    <tr><th>Method</th><th>Path</th><th>Description</th></tr>
    <tr><td>GET</td><td>/wishlists</td><td>List wishlists</td></tr>
    <tr><td>POST</td><td>/wishlists</td><td>Create a wishlist</td></tr>
    <tr><td>GET</td><td>/wishlists/{wishlist_id}</td><td>Get one wishlist</td></tr>
    <tr><td>PUT</td><td>/wishlists/{wishlist_id}</td><td>Update wishlist name/description</td></tr>
    <tr><td>DELETE</td><td>/wishlists/{wishlist_id}</td><td>Delete a wishlist</td></tr>
  </table>
  <h2>Wishlist Items</h2>
  <table border="1" cellpadding="8" cellspacing="0">
    <tr><th>Method</th><th>Path</th><th>Description</th></tr>
    <tr><td>GET</td><td>/wishlists/{wishlist_id}/items</td><td>List items in a wishlist</td></tr>
    <tr><td>POST</td><td>/wishlists/{wishlist_id}/items</td><td>Create an item in a wishlist</td></tr>
    <tr><td>GET</td><td>/wishlists/{wishlist_id}/items/{item_id}</td><td>Get one item in a wishlist</td></tr>
    <tr><td>PUT</td><td>/wishlists/{wishlist_id}/items/{item_id}</td><td>Update item in wishlist</td></tr>
    <tr><td>DELETE</td><td>/wishlists/{wishlist_id}/items/{item_id}</td><td>Delete item from wishlist</td></tr>
  </table>
</body>
</html>"""
