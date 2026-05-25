/**
 * Profile page: view/edit user information and change password.
 */

document.addEventListener("DOMContentLoaded", async () => {
  if (!isLoggedIn()) { window.location.href = "/static/auth.html"; return; }
  await loadProfile();

  document.getElementById("profile-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    clearAlert("profile-alert");
    const data = {
      first_name: document.getElementById("p-first-name").value.trim() || null,
      last_name: document.getElementById("p-last-name").value.trim() || null,
      phone: document.getElementById("p-phone").value.trim() || null,
      address: document.getElementById("p-address").value.trim() || null,
      email: document.getElementById("p-email").value.trim() || null,
    };
    try {
      await apiFetch("/profile", { method: "PUT", body: JSON.stringify(data) });
      showAlert("profile-alert", "Profile updated successfully!", "success");
    } catch (err) {
      showAlert("profile-alert", err.message);
    }
  });

  document.getElementById("password-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    clearAlert("password-alert");
    const current_password = document.getElementById("current-password").value;
    const new_password = document.getElementById("new-password").value;
    const confirm = document.getElementById("confirm-password").value;

    if (new_password.length < 8) {
      showAlert("password-alert", "New password must be at least 8 characters");
      return;
    }
    if (new_password !== confirm) {
      showAlert("password-alert", "Passwords do not match");
      return;
    }
    try {
      await apiFetch("/profile/password", {
        method: "PUT",
        body: JSON.stringify({ current_password, new_password }),
      });
      showAlert("password-alert", "Password changed successfully!", "success");
      document.getElementById("password-form").reset();
    } catch (err) {
      showAlert("password-alert", err.message);
    }
  });
});

async function loadProfile() {
  try {
    const profile = await apiFetch("/profile");
    document.getElementById("p-first-name").value = profile.first_name || "";
    document.getElementById("p-last-name").value = profile.last_name || "";
    document.getElementById("p-email").value = profile.email || "";
    document.getElementById("p-phone").value = profile.phone || "";
    document.getElementById("p-address").value = profile.address || "";
    document.getElementById("p-member-since").textContent = new Date(profile.created_at).toLocaleDateString();
    if (profile.is_admin) {
      document.getElementById("p-admin-badge").style.display = "inline-block";
    }
  } catch (err) {
    showAlert("profile-alert", "Failed to load profile: " + err.message);
  }
}
