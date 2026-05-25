/**
 * Cart page: display items, update quantities, remove items, show totals.
 */

document.addEventListener("DOMContentLoaded", async () => {
  if (!isLoggedIn()) { window.location.href = "/static/auth.html"; return; }
  await loadCart();

  document.getElementById("clear-cart-btn").addEventListener("click", async () => {
    if (!confirm("Clear all items from your cart?")) return;
    try {
      await apiFetch("/cart", { method: "DELETE" });
      await loadCart();
      updateCartBadge();
    } catch (err) {
      showAlert("cart-alert", err.message);
    }
  });
});

async function loadCart() {
  const container = document.getElementById("cart-items");
  container.innerHTML = `<div class="empty-state"><div class="spinner"></div></div>`;
  try {
    const cart = await apiFetch("/cart");
    renderCart(cart);
  } catch (err) {
    container.innerHTML = `<div class="empty-state"><h3>Failed to load cart</h3></div>`;
  }
}

function renderCart(cart) {
  const container = document.getElementById("cart-items");
  const summary = document.getElementById("cart-summary");

  if (cart.items.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <h3>Your cart is empty</h3>
        <p>Browse our <a href="/static/index.html">furniture collection</a> to add items.</p>
      </div>`;
    summary.innerHTML = "";
    document.getElementById("clear-cart-btn").style.display = "none";
    return;
  }

  document.getElementById("clear-cart-btn").style.display = "";

  container.innerHTML = cart.items.map(item => `
    <div class="cart-item" id="cart-item-${item.product.id}">
      <img src="${item.product.image_url || 'https://placehold.co/100x80/E8E0D5/8B6F47?text=+'}" alt="${escHtml(item.product.name)}">
      <div>
        <div class="cart-item-name">
          <a href="/static/product.html?id=${item.product.id}">${escHtml(item.product.name)}</a>
        </div>
        <div class="cart-item-price">$${Number(item.product.price).toFixed(2)} each</div>
        <div class="qty-control">
          <button onclick="changeQty(${item.product.id}, ${item.quantity - 1})">−</button>
          <span>${item.quantity}</span>
          <button onclick="changeQty(${item.product.id}, ${item.quantity + 1})">+</button>
        </div>
      </div>
      <div>
        <div style="font-weight:700;margin-bottom:0.5rem;">$${(Number(item.product.price) * item.quantity).toFixed(2)}</div>
        <button class="btn btn-danger btn-sm" onclick="removeItem(${item.product.id})">Remove</button>
      </div>
    </div>
  `).join("");

  summary.innerHTML = `
    <div class="summary-row"><span>Items (${cart.total_items})</span><span>$${Number(cart.total_price).toFixed(2)}</span></div>
    <div class="summary-row"><span>Shipping</span><span>Free</span></div>
    <div class="summary-row total"><span>Total</span><span>$${Number(cart.total_price).toFixed(2)}</span></div>
    <button class="btn btn-primary btn-full" style="margin-top:1rem" onclick="alert('Checkout flow coming soon!')">Proceed to Checkout</button>
  `;
}

async function changeQty(productId, newQty) {
  if (newQty < 1) { removeItem(productId); return; }
  try {
    const cart = await apiFetch(`/cart/items/${productId}`, {
      method: "PUT",
      body: JSON.stringify({ quantity: newQty }),
    });
    renderCart(cart);
    updateCartBadge();
  } catch (err) { showAlert("cart-alert", err.message); }
}

async function removeItem(productId) {
  try {
    const cart = await apiFetch(`/cart/items/${productId}`, { method: "DELETE" });
    renderCart(cart);
    updateCartBadge();
  } catch (err) { showAlert("cart-alert", err.message); }
}

function escHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
