/**
 * Shared API utilities: fetch wrapper with JWT injection, token storage helpers.
 */

const API_BASE = "/api/v1";

function getToken() { return localStorage.getItem("access_token"); }
function getRefreshToken() { return localStorage.getItem("refresh_token"); }

function saveTokens(data) {
  localStorage.setItem("access_token", data.access_token);
  localStorage.setItem("refresh_token", data.refresh_token);
}

function clearTokens() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("user_email");
}

function isLoggedIn() { return !!getToken(); }

async function apiFetch(path, options = {}) {
  const token = getToken();
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(API_BASE + path, { ...options, headers });

  if (res.status === 401) {
    // Attempt token refresh once
    const refreshed = await tryRefresh();
    if (refreshed) {
      headers["Authorization"] = `Bearer ${getToken()}`;
      const retry = await fetch(API_BASE + path, { ...options, headers });
      if (!retry.ok) {
        if (retry.status === 401) { clearTokens(); window.location.href = "/static/auth.html"; }
        throw await buildError(retry);
      }
      return retry.status === 204 ? null : retry.json();
    }
    clearTokens();
    window.location.href = "/static/auth.html";
    throw new Error("Unauthorized");
  }

  if (!res.ok) throw await buildError(res);
  return res.status === 204 ? null : res.json();
}

async function tryRefresh() {
  const rt = getRefreshToken();
  if (!rt) return false;
  try {
    const res = await fetch(API_BASE + "/auth/refresh", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: rt }),
    });
    if (!res.ok) return false;
    const data = await res.json();
    saveTokens(data);
    return true;
  } catch { return false; }
}

async function buildError(res) {
  let detail = `HTTP ${res.status}`;
  try { const body = await res.json(); detail = body.detail || detail; } catch {}
  const err = new Error(detail);
  err.status = res.status;
  return err;
}

function showAlert(containerId, message, type = "error") {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
}

function clearAlert(containerId) {
  const el = document.getElementById(containerId);
  if (el) el.innerHTML = "";
}

function updateNavAuth() {
  const loginLink = document.getElementById("nav-login");
  const logoutLink = document.getElementById("nav-logout");
  const profileLink = document.getElementById("nav-profile");
  const adminLink = document.getElementById("nav-admin");
  if (isLoggedIn()) {
    if (loginLink) loginLink.style.display = "none";
    if (logoutLink) logoutLink.style.display = "";
    if (profileLink) profileLink.style.display = "";
    const isAdmin = localStorage.getItem("is_admin") === "true";
    if (adminLink) adminLink.style.display = isAdmin ? "" : "none";
  } else {
    if (loginLink) loginLink.style.display = "";
    if (logoutLink) logoutLink.style.display = "none";
    if (profileLink) profileLink.style.display = "none";
    if (adminLink) adminLink.style.display = "none";
  }
}

async function updateCartBadge() {
  const badge = document.getElementById("nav-cart-badge");
  if (!badge || !isLoggedIn()) { if (badge) badge.textContent = ""; return; }
  try {
    const cart = await apiFetch("/cart");
    badge.textContent = cart.total_items > 0 ? cart.total_items : "";
  } catch { badge.textContent = ""; }
}

document.addEventListener("DOMContentLoaded", () => {
  updateNavAuth();
  updateCartBadge();

  const logoutBtn = document.getElementById("nav-logout");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", (e) => {
      e.preventDefault();
      clearTokens();
      window.location.href = "/static/auth.html";
    });
  }
});
