/**
 * Authentication page: login and register tab logic.
 */

document.addEventListener("DOMContentLoaded", () => {
  if (isLoggedIn()) { window.location.href = "/static/index.html"; return; }

  const tabs = document.querySelectorAll(".auth-tab");
  const loginForm = document.getElementById("login-form");
  const registerForm = document.getElementById("register-form");

  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");
      clearAlert("auth-alert");
      if (tab.dataset.tab === "login") {
        loginForm.style.display = "";
        registerForm.style.display = "none";
      } else {
        loginForm.style.display = "none";
        registerForm.style.display = "";
      }
    });
  });

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    clearAlert("auth-alert");
    const email = document.getElementById("login-email").value.trim();
    const password = document.getElementById("login-password").value;
    try {
      const data = await apiFetch("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      saveTokens(data);
      await fetchAndStoreProfile();
      window.location.href = "/static/index.html";
    } catch (err) {
      showAlert("auth-alert", err.message);
    }
  });

  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    clearAlert("auth-alert");
    const email = document.getElementById("reg-email").value.trim();
    const password = document.getElementById("reg-password").value;
    const first_name = document.getElementById("reg-first-name").value.trim() || null;
    const last_name = document.getElementById("reg-last-name").value.trim() || null;

    if (password.length < 8) {
      showAlert("auth-alert", "Password must be at least 8 characters");
      return;
    }

    try {
      const data = await apiFetch("/auth/register", {
        method: "POST",
        body: JSON.stringify({ email, password, first_name, last_name }),
      });
      saveTokens(data);
      await fetchAndStoreProfile();
      window.location.href = "/static/index.html";
    } catch (err) {
      showAlert("auth-alert", err.message);
    }
  });
});

async function fetchAndStoreProfile() {
  try {
    const profile = await apiFetch("/profile");
    localStorage.setItem("is_admin", profile.is_admin);
    localStorage.setItem("user_email", profile.email);
  } catch {}
}
