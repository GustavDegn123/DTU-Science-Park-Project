document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem("access_token");
    console.log("📌 Stored token:", token); // Debugging

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
            const errorText = await userResponse.text();
            throw new Error(`Failed to fetch user data: ${errorText}`);
        }

        const user = await userResponse.json();
        console.log("✅ User data received:", user); // Debug user data

        document.getElementById("welcomeMessage").textContent = `Welcome, ${user.firstname} ${user.lastname}!`;

        if (user.user_type === "company") {
            console.log("✅ Company detected. Loading startups & investments...");
            loadCompanyStartups();
            loadCompanyInvestments();
        } else {
            console.warn("⚠️ User is not a company, redirecting...");
            window.location.href = "/dashboard_investor"; // Redirect til investor-dashboard
        }

    } catch (error) {
        console.error("❌ Error loading user data:", error);
        document.getElementById("welcomeMessage").textContent = "⚠️ Failed to load user data";
    }
});

// 🔹 Hent startups for virksomheder
// 🔹 Hent startups inkl. impact score
async function loadCompanyStartups() {
    try {
        const response = await fetch("/startups/my-startups", {
            headers: { "Authorization": `Bearer ${localStorage.getItem("access_token")}` }
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch company startups: ${response.statusText}`);
        }

        const startups = await response.json();
        const container = document.getElementById("startupInvestmentContainer");
        container.innerHTML = "";

        if (startups.length === 0) {
            container.innerHTML = "<p>No startups created yet.</p>";
            return;
        }

        startups.forEach(s => {
            const div = document.createElement("div");
            div.classList.add("startup-card");
            div.innerHTML = `
                <h3>${s.name}</h3>
                <p>${s.description}</p>
                <p><b>Impact Score:</b> ${s.impact_score ?? "N/A"}</p>
                <p><b>ESG Score:</b> ${s.esg_score ?? "N/A"}</p>
                <p><b>Traction:</b> ${s.traction ?? "N/A"}</p>
            `;
            container.appendChild(div);
        });

    } catch (error) {
        console.error("❌ Error loading startups:", error);
        document.getElementById("startupInvestmentContainer").innerHTML = "<p>Error loading startups.</p>";
    }
}

// 🔹 Hent investeringer modtaget af virksomheden
async function loadCompanyInvestments() {
    try {
        const response = await fetch("/investments/company-investments", {
            headers: { "Authorization": `Bearer ${localStorage.getItem("access_token")}` }
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch company investments: ${response.statusText}`);
        }

        const investments = await response.json();
        console.log("✅ Company received investments:", investments); // Debug

        const container = document.getElementById("receivedInvestmentContainer");
        container.innerHTML = "";

        if (investments.length === 0) {
            container.innerHTML = "<p>No investments received yet.</p>";
            return;
        }

        investments.forEach(inv => {
            const div = document.createElement("div");
            div.classList.add("investment-card");
            div.innerHTML = `
                <h3>Investment in ${inv.startup_name}</h3>
                <p><b>Amount:</b> €${inv.amount}</p>
                <p><b>Investor ID:</b> ${inv.investor_id}</p>
            `;
            container.appendChild(div);
        });

    } catch (error) {
        console.error("❌ Error loading company investments:", error);
        document.getElementById("receivedInvestmentContainer").innerHTML = "<p>Error loading investments.</p>";
    }
}

