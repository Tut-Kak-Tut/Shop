/**
 * Shop catalog page: product grid, filters, search, pagination.
 */

let currentPage = 1;
let searchTimeout = null;

document.addEventListener("DOMContentLoaded", async () => {
  await loadCategories();
  await loadProducts();

  // Search with debounce
  document.getElementById("search-input").addEventListener("input", () => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => { currentPage = 1; loadProducts(); }, 400);
  });

  document.getElementById("filter-form").addEventListener("submit", (e) => {
    e.preventDefault();
    currentPage = 1;
    loadProducts();
  });

  document.getElementById("filter-reset").addEventListener("click", () => {
    document.getElementById("filter-form").reset();
    document.getElementById("search-input").value = "";
    currentPage = 1;
    loadProducts();
  });

  document.getElementById("sort-select").addEventListener("change", () => {
    currentPage = 1;
    loadProducts();
  });
});

async function loadCategories() {
  try {
    const cats = await apiFetch("/products/categories");
    const select = document.getElementById("filter-category");
    cats.forEach(cat => {
      const opt = document.createElement("option");
      opt.value = cat.slug;
      opt.textContent = cat.name;
      select.appendChild(opt);
    });
  } catch {}
}

async function loadProducts() {
  const grid = document.getElementById("product-grid");
  grid.innerHTML = `<div class="empty-state"><div class="spinner"></div></div>`;

  const params = buildParams();

  try {
    const data = await apiFetch("/products?" + params.toString());
    renderProducts(data);
    renderPagination(data);
    document.getElementById("result-count").textContent = `${data.total} products found`;
  } catch (err) {
    grid.innerHTML = `<div class="empty-state"><h3>Failed to load products</h3><p>${err.message}</p></div>`;
  }
}

function buildParams() {
  const params = new URLSearchParams();
  const search = document.getElementById("search-input").value.trim();
  if (search) params.set("search", search);

  const cat = document.getElementById("filter-category").value;
  if (cat) params.set("category", cat);

  const minPrice = document.getElementById("filter-min-price").value;
  if (minPrice) params.set("min_price", minPrice);

  const maxPrice = document.getElementById("filter-max-price").value;
  if (maxPrice) params.set("max_price", maxPrice);

  const material = document.getElementById("filter-material").value.trim();
  if (material) params.set("material", material);

  const color = document.getElementById("filter-color").value.trim();
  if (color) params.set("color", color);

  const sort = document.getElementById("sort-select").value;
  if (sort) params.set("sort", sort);

  params.set("page", currentPage);
  params.set("limit", 12);
  return params;
}

function renderProducts(data) {
  const grid = document.getElementById("product-grid");
  if (data.items.length === 0) {
    grid.innerHTML = `<div class="empty-state" style="grid-column:1/-1"><h3>No products found</h3><p>Try adjusting your filters or search query.</p></div>`;
    return;
  }
  grid.innerHTML = data.items.map(p => `
    <div class="card product-card" onclick="window.location='/static/product.html?id=${p.id}'">
      <img src="${p.image_url || 'https://placehold.co/400x300/E8E0D5/8B6F47?text=No+Image'}" alt="${escHtml(p.name)}" loading="lazy">
      <div class="product-card-body">
        <div class="product-card-cat">${p.category ? escHtml(p.category.name) : ''}</div>
        <div class="product-card-name">${escHtml(p.name)}</div>
        <div class="product-card-price">$${Number(p.price).toFixed(2)}</div>
      </div>
    </div>
  `).join("");
}

function renderPagination(data) {
  const el = document.getElementById("pagination");
  el.innerHTML = "";
  if (data.pages <= 1) return;

  const prev = document.createElement("button");
  prev.textContent = "← Prev";
  prev.disabled = currentPage <= 1;
  prev.addEventListener("click", () => { currentPage--; loadProducts(); });
  el.appendChild(prev);

  for (let i = 1; i <= data.pages; i++) {
    if (data.pages > 7 && Math.abs(i - currentPage) > 2 && i !== 1 && i !== data.pages) continue;
    const btn = document.createElement("button");
    btn.textContent = i;
    if (i === currentPage) btn.classList.add("active");
    btn.addEventListener("click", () => { currentPage = i; loadProducts(); });
    el.appendChild(btn);
  }

  const next = document.createElement("button");
  next.textContent = "Next →";
  next.disabled = currentPage >= data.pages;
  next.addEventListener("click", () => { currentPage++; loadProducts(); });
  el.appendChild(next);
}

function escHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
