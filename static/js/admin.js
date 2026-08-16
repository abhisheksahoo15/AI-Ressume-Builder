const profileFields = [
    ["profileName", "name"],
    ["profileEmail", "email"],
    ["profilePhone", "phone"],
    ["profileLinkedin", "linkedin"],
    ["profileEducation", "education"],
    ["profileExperience", "experience"],
    ["profileProjects", "projects"],
    ["profileCertifications", "certifications"]
];

const adminForm = document.getElementById("adminForm");
const adminStatus = document.getElementById("adminStatus");
const temperatureInput = document.getElementById("analysisTemperature");
const minimumScoreInput = document.getElementById("minimumScore");
const adminLoginCard = document.getElementById("adminLoginCard");
const adminWorkspace = document.getElementById("adminWorkspace");
const adminLoginForm = document.getElementById("adminLoginForm");
const adminLoginStatus = document.getElementById("adminLoginStatus");

function showLoginStatus(message, type = "error") {
    adminLoginStatus.textContent = message;
    adminLoginStatus.className = `admin-feedback ${type}`;
}

function setAuthenticated(authenticated) {
    adminLoginCard.hidden = authenticated;
    adminWorkspace.hidden = !authenticated;
    if (authenticated) loadAdminSettings();
}

function showAdminStatus(message, type = "success") {
    adminStatus.textContent = message;
    adminStatus.className = `admin-feedback ${type}`;
    window.clearTimeout(showAdminStatus.timer);
    showAdminStatus.timer = window.setTimeout(() => {
        adminStatus.textContent = "";
        adminStatus.className = "admin-feedback";
    }, 4200);
}

function updateTemperatureLabel() {
    const value = Number(temperatureInput.value || 0).toFixed(2);
    document.getElementById("temperatureValue").textContent = value;
}

function updateSummary() {
    const completed = profileFields.filter(([id]) => document.getElementById(id).value.trim()).length;
    document.getElementById("profileFieldCount").textContent = `${completed} / ${profileFields.length}`;
    document.getElementById("summaryRole").textContent = document.getElementById("targetRole").value.trim() || "Not set";
    const score = Math.max(0, Math.min(100, Number(minimumScoreInput.value || 0)));
    document.getElementById("minimumScoreValue").textContent = `${score}%`;
    document.getElementById("summaryThreshold").textContent = `${score}%`;
}

function fillAdminForm(settings) {
    const profile = settings.profile || {};
    const ats = settings.ats || {};
    profileFields.forEach(([id, key]) => {
        document.getElementById(id).value = profile[key] || "";
    });
    document.getElementById("targetRole").value = ats.target_role || "";
    minimumScoreInput.value = ats.minimum_ats_score ?? 70;
    temperatureInput.value = ats.analysis_temperature ?? 0.35;
    document.getElementById("reviewNotes").value = ats.review_notes || "";
    updateTemperatureLabel();
    updateSummary();
}

async function loadAdminSettings() {
    try {
        const response = await fetch("/api/admin/settings/");
        if (response.status === 401) {
            setAuthenticated(false);
            return;
        }
        if (!response.ok) throw new Error("Unable to load settings");
        const data = await response.json();
        fillAdminForm(data.settings);
    } catch (error) {
        showAdminStatus("Settings could not be loaded. The default workspace is ready.", "error");
    }
}

async function loadAdminSession() {
    try {
        const response = await fetch("/api/admin/session/");
        setAuthenticated(response.ok);
    } catch (error) {
        setAuthenticated(false);
    }
}

function collectAdminSettings() {
    const profile = {};
    profileFields.forEach(([id, key]) => {
        profile[key] = document.getElementById(id).value.trim();
    });
    return {
        profile,
        ats: {
            target_role: document.getElementById("targetRole").value.trim(),
            minimum_ats_score: Number(minimumScoreInput.value || 70),
            analysis_temperature: Number(temperatureInput.value || 0.35),
            review_notes: document.getElementById("reviewNotes").value.trim()
        }
    };
}

adminForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
        const response = await fetch("/api/admin/settings/", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(collectAdminSettings())
        });
        if (response.status === 401) {
            setAuthenticated(false);
            showLoginStatus("Your session has expired. Please sign in again.");
            return;
        }
        if (!response.ok) throw new Error("Unable to save settings");
        const data = await response.json();
        fillAdminForm(data.settings);
        showAdminStatus("Workspace settings saved successfully.");
    } catch (error) {
        showAdminStatus("Settings could not be saved. Please try again.", "error");
    }
});

document.getElementById("resetAdmin").addEventListener("click", async () => {
    if (!window.confirm("Reset the resume profile and ATS preferences?")) return;
    try {
        const response = await fetch("/api/admin/reset/", { method: "POST" });
        if (response.status === 401) {
            setAuthenticated(false);
            showLoginStatus("Your session has expired. Please sign in again.");
            return;
        }
        if (!response.ok) throw new Error("Unable to reset settings");
        const data = await response.json();
        fillAdminForm(data.settings);
        showAdminStatus("Workspace reset to its default settings.");
    } catch (error) {
        showAdminStatus("Workspace could not be reset. Please try again.", "error");
    }
});

temperatureInput.addEventListener("input", () => {
    updateTemperatureLabel();
    updateSummary();
});
minimumScoreInput.addEventListener("input", updateSummary);
profileFields.forEach(([id]) => document.getElementById(id).addEventListener("input", updateSummary));
document.getElementById("targetRole").addEventListener("input", updateSummary);

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
        adminLoginForm.reset();
        setAuthenticated(true);
    } catch (error) {
        showLoginStatus("Invalid username or password. Please try again.");
    }
});

document.getElementById("adminLogout").addEventListener("click", async () => {
    await fetch("/api/admin/logout/", { method: "POST" });
    setAuthenticated(false);
    showLoginStatus("You have been signed out.", "success");
});

loadAdminSession();
