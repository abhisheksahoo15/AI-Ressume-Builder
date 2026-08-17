document.addEventListener("DOMContentLoaded", function () {

    const welcomeGate = document.getElementById("welcomeGate");
    const welcomeTypewriter = document.getElementById("welcomeTypewriter");
    const welcomeEnterBtn = document.getElementById("welcomeEnterBtn");
    const welcomeParticleField = document.getElementById("welcomeParticleField");
    const welcomeGoogleBtn = document.getElementById("welcomeGoogleBtn");
    const welcomeGoogleButtonText = document.getElementById("welcomeGoogleButtonText");
    const welcomeSignedIn = document.getElementById("welcomeSignedIn");
    const welcomeSignedInEmail = document.getElementById("welcomeSignedInEmail");
    const demoAuthModal = document.getElementById("demoAuthModal");
    const demoAuthClose = document.getElementById("demoAuthClose");
    const demoAuthForm = document.getElementById("demoAuthForm");
    const demoGmail = document.getElementById("demoGmail");
    const demoAuthStatus = document.getElementById("demoAuthStatus");
    const demoAuthStorageKey = "hirefire_demo_user";

    const setDemoAuthStatus = (message, type = "") => {
        if (!demoAuthStatus) return;
        demoAuthStatus.textContent = message;
        demoAuthStatus.className = `demo-auth-status${type ? ` ${type}` : ""}`;
    };

    const applyDemoUser = (email) => {
        if (!email) return;
        if (welcomeGoogleButtonText) welcomeGoogleButtonText.textContent = "Signed in with Google";
        if (welcomeGoogleBtn) welcomeGoogleBtn.classList.add("is-signed-in");
        if (welcomeSignedInEmail) welcomeSignedInEmail.textContent = email;
        if (welcomeSignedIn) welcomeSignedIn.hidden = false;
    };

    const closeDemoAuth = () => {
        if (!demoAuthModal) return;
        demoAuthModal.hidden = true;
        setDemoAuthStatus("");
    };

    if (welcomeGate && welcomeTypewriter && welcomeEnterBtn) {
        document.body.classList.add("welcome-active");
        welcomeEnterBtn.disabled = false;
        welcomeEnterBtn.textContent = "Enter platform";
        welcomeTypewriter.textContent = "";

        const particleColors = ["#f9a8d4", "#c084fc", "#7dd3fc", "#fde68a"];
        if (welcomeParticleField) {
            for (let i = 0; i < 54; i += 1) {
                const particle = document.createElement("span");
                particle.className = "welcome-particle";
                particle.style.setProperty("--particle-left", `${Math.random() * 100}%`);
                particle.style.setProperty("--particle-top", `${Math.random() * 100}%`);
                particle.style.setProperty("--particle-size", `${Math.random() * 3 + 2}px`);
                particle.style.setProperty("--particle-x", `${Math.random() * 90 - 45}px`);
                particle.style.setProperty("--particle-duration", `${Math.random() * 8 + 8}s`);
                particle.style.setProperty("--particle-delay", `${Math.random() * -10}s`);
                particle.style.setProperty("--particle-color", particleColors[i % particleColors.length]);
                welcomeParticleField.appendChild(particle);
            }
        }

        const disclaimerText = "HireFire AI brings resume creation, ATS analysis, and job discovery into one focused workspace for ambitious professionals.";
        let typedIndex = 0;
        let typingTimer = null;
        let typingDone = false;

        const finishTyping = () => {
            if (typingDone) return;
            typingDone = true;
            if (typingTimer) {
                window.clearTimeout(typingTimer);
            }
            welcomeTypewriter.textContent = disclaimerText;
            welcomeGate.classList.add("typing-complete");
            welcomeEnterBtn.disabled = false;
            welcomeEnterBtn.textContent = "Enter platform";
        };

        const typeDisclaimer = () => {
            if (typingDone) return;
            typedIndex += 1;
            welcomeTypewriter.textContent = disclaimerText.slice(0, typedIndex);
            if (typedIndex < disclaimerText.length) {
                typingTimer = window.setTimeout(typeDisclaimer, typedIndex < 40 ? 24 : 15);
            } else {
                finishTyping();
            }
        };

        const landHome = () => {
            if (welcomeGate.classList.contains("welcome-leaving")) return;
            finishTyping();
            welcomeEnterBtn.disabled = true;
            welcomeGate.classList.add("welcome-flashing");
            window.setTimeout(() => {
                welcomeGate.classList.add("welcome-leaving");
                document.body.classList.remove("welcome-active");
            }, 620);
            window.setTimeout(() => {
                welcomeGate.remove();
            }, 1300);
        };

        welcomeEnterBtn.addEventListener("click", landHome);

        if (welcomeGoogleBtn && demoAuthModal && demoAuthForm && demoGmail) {
            let savedDemoUser = "";
            try {
                savedDemoUser = window.localStorage.getItem(demoAuthStorageKey) || "";
            } catch (error) {
                savedDemoUser = "";
            }
            applyDemoUser(savedDemoUser);

            welcomeGoogleBtn.addEventListener("click", () => {
                demoAuthModal.hidden = false;
                window.setTimeout(() => demoGmail.focus(), 0);
            });

            demoAuthForm.addEventListener("submit", (event) => {
                event.preventDefault();
                const email = demoGmail.value.trim().toLowerCase();
                if (!/^[^\s@]+@gmail\.com$/.test(email)) {
                    setDemoAuthStatus("Please enter a valid Gmail address.", "error");
                    demoGmail.focus();
                    return;
                }

                try {
                    window.localStorage.setItem(demoAuthStorageKey, email);
                } catch (error) {
                    // The showcase still works when browser storage is unavailable.
                }
                applyDemoUser(email);
                closeDemoAuth();
            });

            if (demoAuthClose) demoAuthClose.addEventListener("click", closeDemoAuth);
            demoAuthModal.querySelectorAll("[data-demo-auth-close]").forEach((element) => {
                element.addEventListener("click", closeDemoAuth);
            });
            document.addEventListener("keydown", (event) => {
                if (event.key === "Escape" && !demoAuthModal.hidden) closeDemoAuth();
            });
        }

        document.addEventListener("keydown", (event) => {
            if ((event.key === "Enter" || event.key === " ") && (!demoAuthModal || demoAuthModal.hidden)) {
                landHome();
            }
        });

        typingTimer = window.setTimeout(typeDisclaimer, 120);
    }
    const revealElements = document.querySelectorAll(".reveal");

    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("visible");
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.15 }
        );

        revealElements.forEach((element) => observer.observe(element));
    } else {
        revealElements.forEach((element) => element.classList.add("visible"));
    }

    const lineCanvas = document.getElementById("lineChart");
    const barCanvas = document.getElementById("barChart");

    if (lineCanvas && typeof Chart !== "undefined") {
        const lineCtx = lineCanvas.getContext("2d");
        const lineData = [10, 20, 15, 30, 40, 25, 50];
        const lineChart = new Chart(lineCtx, {
            type: "line",
            data: {
                labels: ["AI & ML", "Blockchain", "Mobile", "FinTech", "Others"],
                datasets: [
                    {
                        label: "Dynamic Enrollments",
                        data: lineData,
                        backgroundColor: "rgba(255, 87, 34, 0.2)",
                        borderColor: "#ff5722",
                        borderWidth: 2,
                        tension: 0.4,
                    },
                ],
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true } },
            },
        });

        setInterval(() => {
            lineData.forEach((_, i) => (lineData[i] += Math.floor(Math.random() * 15)));
            lineChart.update();
        }, 2000);
    }

    if (barCanvas && typeof Chart !== "undefined") {
        const barCtx = barCanvas.getContext("2d");
        const bins = Array.from({ length: 20 }, (_, i) => i + 1);
        const binData = Array.from({ length: 20 }, () => Math.floor(Math.random() * 100));
        const barChart = new Chart(barCtx, {
            type: "bar",
            data: {
                labels: bins,
                datasets: [
                    {
                        label: "Category Distribution",
                        data: binData,
                        backgroundColor: "rgba(54, 162, 235, 0.8)",
                        borderColor: "#36a2eb",
                        borderWidth: 1,
                    },
                ],
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true } },
            },
        });

        setInterval(() => {
            binData.forEach((_, i) => (binData[i] = Math.floor(Math.random() * 100)));
            barChart.update();
        }, 2000);
    }
});
