/**
 * Admin panel: manage products and categories.
 */

let categories = [];
let editingProductId = null;

document.addEventListener("DOMContentLoaded", async () => {
  if (!isLoggedIn()) { window.location.href = "/static/auth.html"; return; }
  if (localStorage.getItem("is_admin") !== "true") {
    document.body.innerHTML = `<div class="container" style="padding:4rem 1rem;text-align:center"><h2>Access denied</h2><p>Admin privileges required.</p><a href="/static/index.html">Go home</a></div>`;
    return;
  }

  await loadCategories();
  await loadProducts();

  document.querySelectorAll(".admin-tab").forEach(tab => {
    tab.addEventListener("click", () => {
      document.querySelectorAll(".admin-tab").forEach(t => t.classList.remove("active"));
      tab.classList.add("active");
      document.querySelectorAll(".admin-panel").forEach(p => p.style.display = "none");
      document.getElementById("panel-" + tab.dataset.tab).style.display = "";
    });
  });

  document.getElementById("add-product-btn").addEventListener("click", () => openProductModal(null));
  document.getElementById("product-form").addEventListener("submit", submitProduct);

  document.getElementById("category-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    clearAlert("cat-alert");
    const name = document.getElementById("cat-name").value.trim();
    const slug = document.getElementById("cat-slug").value.trim();
    try {
      await apiFetch("/admin/categories", { method: "POST", body: JSON.stringify({ name, slug }) });
      showAlert("cat-alert", "Category created!", "success");
      document.getElementById("category-form").reset();
      await loadCategories();
    } catch (err) { showAlert("cat-alert", err.message); }
  });

  document.getElementById("modal-cancel").addEventListener("click", closeModal);
  document.getElementById("modal-overlay").addEventListener("click", (e) => {
    if (e.target === document.getElementById("modal-overlay")) closeModal();
  });

  // Image picker events
  document.getElementById("btn-choose-img").addEventListener("click", () => {
    document.getElementById("modal-image-file").click();
  });

  document.getElementById("modal-image-file").addEventListener("change", async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const status = document.getElementById("img-upload-status");
    status.textContent = "Uploading…";
    clearAlert("modal-alert");

    const formData = new FormData();
    formData.append("file", file);
    try {
      const token = getToken();
      const res = await fetch("/api/v1/admin/upload-image", {
        method: "POST",
        headers: token ? { "Authorization": `Bearer ${token}` } : {},
        body: formData,
      });
      if (!res.ok) { const err = await res.json(); throw new Error(err.detail); }
      const data = await res.json();
      document.getElementById("modal-image-url").value = data.url;
      document.getElementById("modal-image-url-text").value = data.url;
      setImagePreview(data.url);
      status.textContent = "Uploaded!";
      setTimeout(() => { status.textContent = ""; }, 2000);
    } catch (err) {
      status.textContent = "";
      showAlert("modal-alert", "Upload failed: " + err.message);
    }
  });

  document.getElementById("modal-image-url-text").addEventListener("input", (e) => {
    const val = e.target.value.trim();
    document.getElementById("modal-image-url").value = val;
    setImagePreview(val || null);
  });

  document.getElementById("btn-remove-img").addEventListener("click", () => {
    document.getElementById("modal-image-url").value = "";
    document.getElementById("modal-image-url-text").value = "";
    document.getElementById("modal-image-file").value = "";
    setImagePreview(null);
  });
});

async function loadCategories() {
  try {
    categories = await apiFetch("/products/categories");
    const select = document.getElementById("modal-category");
    select.innerHTML = `<option value="">— No category —</option>` +
      categories.map(c => `<option value="${c.id}">${c.name}</option>`).join("");

    const list = document.getElementById("cat-list");
    list.innerHTML = categories.length === 0
      ? `<div class="empty-state"><h3>No categories yet</h3></div>`
      : `<table class="admin-table">
           <thead><tr><th>ID</th><th>Name</th><th>Slug</th><th>Actions</th></tr></thead>
           <tbody>
             ${categories.map(c => `
               <tr>
                 <td>${c.id}</td>
                 <td>${c.name}</td>
                 <td>${c.slug}</td>
                 <td><button class="btn btn-danger btn-sm" onclick="deleteCategory(${c.id})">Delete</button></td>
               </tr>`).join("")}
           </tbody>
         </table>`;
  } catch {}
}

async function loadProducts() {
  const table = document.getElementById("products-table");
  table.innerHTML = `<div class="empty-state"><div class="spinner"></div></div>`;
  try {
    const data = await apiFetch("/products?limit=100");
    if (data.items.length === 0) {
      table.innerHTML = `<div class="empty-state"><h3>No products yet</h3></div>`;
      return;
    }
    table.innerHTML = `<table class="admin-table">
      <thead><tr><th>ID</th><th>Name</th><th>Category</th><th>Price</th><th>Stock</th><th>Actions</th></tr></thead>
      <tbody>
        ${data.items.map(p => `
          <tr>
            <td>${p.id}</td>
            <td>${p.name}</td>
            <td>${p.category ? p.category.name : "—"}</td>
            <td>$${Number(p.price).toFixed(2)}</td>
            <td>${p.stock}</td>
            <td style="display:flex;gap:0.4rem">
              <button class="btn btn-secondary btn-sm" onclick="openProductModal(${p.id})">Edit</button>
              <button class="btn btn-danger btn-sm" onclick="deleteProduct(${p.id})">Delete</button>
            </td>
          </tr>`).join("")}
      </tbody>
    </table>`;
  } catch (err) {
    table.innerHTML = `<div class="empty-state"><h3>${err.message}</h3></div>`;
  }
}

async function openProductModal(productId) {
  editingProductId = productId;
  document.getElementById("modal-title").textContent = productId ? "Edit Product" : "Add Product";
  document.getElementById("product-form").reset();
  clearAlert("modal-alert");
  setImagePreview(null);
  document.getElementById("modal-image-url").value = "";
  document.getElementById("modal-image-url-text").value = "";
  document.getElementById("modal-image-file").value = "";
  document.getElementById("img-upload-status").textContent = "";

  if (productId) {
    try {
      const p = await apiFetch("/products/" + productId);
      document.getElementById("modal-name").value = p.name;
      document.getElementById("modal-description").value = p.description || "";
      document.getElementById("modal-price").value = p.price;
      document.getElementById("modal-material").value = p.material || "";
      document.getElementById("modal-color").value = p.color || "";
      document.getElementById("modal-stock").value = p.stock;
      document.getElementById("modal-category").value = p.category ? p.category.id : "";
      document.getElementById("modal-image-url").value = p.image_url || "";
      document.getElementById("modal-image-url-text").value = p.image_url || "";
      setImagePreview(p.image_url || null);
    } catch (err) { showAlert("modal-alert", err.message); }
  }

  document.getElementById("modal-overlay").classList.add("open");
}

function closeModal() {
  document.getElementById("modal-overlay").classList.remove("open");
  editingProductId = null;
  setImagePreview(null);
  document.getElementById("modal-image-url").value = "";
  document.getElementById("modal-image-url-text").value = "";
  document.getElementById("modal-image-file").value = "";
}

async function submitProduct(e) {
  e.preventDefault();
  clearAlert("modal-alert");
  const payload = {
    name: document.getElementById("modal-name").value.trim(),
    description: document.getElementById("modal-description").value.trim() || null,
    price: document.getElementById("modal-price").value,
    material: document.getElementById("modal-material").value.trim() || null,
    color: document.getElementById("modal-color").value.trim() || null,
    stock: parseInt(document.getElementById("modal-stock").value),
    image_url: document.getElementById("modal-image-url").value.trim() || null,  // set by file upload or URL text box
    category_id: document.getElementById("modal-category").value || null,
  };

  try {
    if (editingProductId) {
      await apiFetch("/admin/products/" + editingProductId, { method: "PUT", body: JSON.stringify(payload) });
    } else {
      await apiFetch("/admin/products", { method: "POST", body: JSON.stringify(payload) });
    }
    closeModal();
    await loadProducts();
  } catch (err) { showAlert("modal-alert", err.message); }
}

async function deleteProduct(productId) {
  if (!confirm("Delete this product? This action cannot be undone.")) return;
  try {
    await apiFetch("/admin/products/" + productId, { method: "DELETE" });
    await loadProducts();
  } catch (err) { alert(err.message); }
}

async function deleteCategory(categoryId) {
  if (!confirm("Delete this category? Products in this category will become uncategorized.")) return;
  try {
    await apiFetch("/admin/categories/" + categoryId, { method: "DELETE" });
    await loadCategories();
  } catch (err) { alert(err.message); }
}

function setImagePreview(url) {
  const img = document.getElementById("modal-img-preview");
  const placeholder = document.getElementById("modal-img-placeholder");
  const removeBtn = document.getElementById("btn-remove-img");
  if (url) {
    img.src = url;
    img.style.display = "";
    placeholder.style.display = "none";
    removeBtn.style.display = "";
  } else {
    img.src = "";
    img.style.display = "none";
    placeholder.style.display = "";
    removeBtn.style.display = "none";
  }
}
