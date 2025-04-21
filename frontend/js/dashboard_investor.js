document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
        console.error("❌ No token found! Redirecting to login...");
        window.location.href = "/login";
        return;
    }

    try {
        const userResponse = await fetch("/auth/user", {  
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        });

        if (!userResponse.ok) {
            throw new Error(`Failed to fetch user data: ${await userResponse.text()}`);
        }

        const user = await userResponse.json();
        document.getElementById("welcomeMessage").textContent = `Welcome, ${user.firstname} ${user.lastname}!`;

        if (user.user_type === "investor") {
            loadInvestments();
            loadStartups();
        } else {
            loadCompanyStartups();
            loadCompanyInvestments();
        }

    } catch (error) {
        console.error("Error loading user data:", error);
        document.getElementById("welcomeMessage").textContent = "⚠️ Failed to load user data";
    }
});

async function fetchStartupNames() {
    try {
        const response = await fetch("/startups", {
            headers: { "Authorization": `Bearer ${localStorage.getItem("access_token")}` }
        });

        if (!response.ok) {
            throw new Error("Failed to fetch startups");
        }

        const startups = await response.json();
        return startups.reduce((map, s) => {
            map[s.id] = s.name; // Gemmer startup-id som key og navn som værdi
            return map;
        }, {});

    } catch (error) {
        console.error("Error loading startup names:", error);
        return {};
    }
}

async function loadInvestments() {
    try {
        const response = await fetch("/investments/", {
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const investments = await response.json();
        const startupNames = await fetchStartupNames(); // Henter alle startup-navne

        const container = document.getElementById("investmentContainer");
        container.innerHTML = investments.length 
            ? investments.map(inv => `
                <div class="investment-card">
                    <h3>Investment in ${startupNames[inv.startup_id] || "Unknown Startup"}</h3>
                    <p><b>Amount:</b> €${inv.amount}</p>
                </div>
            `).join("") 
            : "<p>No investments found.</p>";

    } catch (error) {
        console.error("Error loading investments:", error);
        document.getElementById("investmentContainer").innerHTML = `<p>Error loading investments.</p>`;
    }
}

async function loadStartups() {
    try {
        const response = await fetch("/startups", {
            headers: { "Authorization": `Bearer ${localStorage.getItem("access_token")}` }
        });

        if (!response.ok) {
            throw new Error("Failed to fetch startups");
        }

        const startups = await response.json();
        const container = document.getElementById("startupContainer");
        container.innerHTML = startups.length 
            ? startups.map(s => `
                <div class="startup-card">
                    <h3>${s.name}</h3>
                    <p>${s.description}</p>
                    <p><b>Impact Score:</b> ${s.impact_score ?? "N/A"}</p>
                    <button class="invest-btn" onclick="invest(${s.id})">Invest</button>
                </div>
            `).join("")
            : "<p>No startups available.</p>";

    } catch (error) {
        console.error("Error loading startups:", error);
    }
}

async function invest(startupId) {
    const payload = { startup_id: startupId, amount: 500 };

    try {
        const response = await fetch("/investments/", { 
            method: "POST",
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Investment failed");
        }

        loadInvestments(); // Opdater listen af investeringer
    } catch (error) {
        console.error("Investment error:", error);
        alert(error.message);
    }
}
