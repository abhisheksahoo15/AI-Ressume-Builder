const adminLoginForm = document.getElementById("adminLoginForm");
const adminLoginStatus = document.getElementById("adminLoginStatus");

function showLoginStatus(message, type = "error") {
    adminLoginStatus.textContent = message;
    adminLoginStatus.className = `admin-feedback ${type}`;
}

adminLoginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    showLoginStatus("Signing in...", "success");
    try {
        const response = await fetch("/api/admin/login/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                username: document.getElementById("adminUsername").value.trim(),
                password: document.getElementById("adminPassword").value
            })
        });
        if (!response.ok) throw new Error("Invalid credentials");
        window.location.href = "/admin/";
    } catch (error) {
        showLoginStatus("Invalid username or password. Please try again.");
    }
});
