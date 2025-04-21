console.log("📌 addStartup.js loaded.");

// Hent HTML-elementer
const startupForm = document.getElementById("startupForm");
const resultArea = document.getElementById("resultArea");

// 🔹 Funktion til at hente Company ID
async function getCompanyId() {
    const token = localStorage.getItem("access_token");
    if (!token) {
        throw new Error("❌ No authentication token found!");
    }

    const response = await fetch("/auth/user", {
        headers: { "Authorization": `Bearer ${token}` }
    });

    if (!response.ok) {
        throw new Error("❌ Failed to fetch company information.");
    }

    const userData = await response.json();
    if (userData.user_type !== "company") {
        throw new Error("❌ Only companies can add startups.");
    }

    return userData.id;
}

// 🔹 Funktion til at oprette en ny startup
async function createStartup(event) {
    event.preventDefault();

    // Hent værdier fra formularen
    const formData = {
        name: document.getElementById("startupName")?.value.trim(),
        description: document.getElementById("startupDesc")?.value.trim(),
        sector: document.getElementById("startupSector")?.value.trim() || null,
        funding_stage: document.getElementById("fundingStage")?.value.trim() || null,
        revenue: parseFloat(document.getElementById("revenue")?.value) || null,
        employees: parseInt(document.getElementById("employees")?.value) || null,
        funding_goal: parseFloat(document.getElementById("fundingGoal")?.value) || null,
        impact_score: parseFloat(document.getElementById("impactScore")?.value) || null,
        esg_score: parseFloat(document.getElementById("esgScore")?.value) || null,
        traction: parseFloat(document.getElementById("traction")?.value) || null,
        funding_history: parseFloat(document.getElementById("fundingHistory")?.value) || null,
        sdg_alignment: parseFloat(document.getElementById("sdgAlignment")?.value) || null,
        funding_sought: parseFloat(document.getElementById("fundingSought")?.value) || 0,
        funding_received: parseFloat(document.getElementById("fundingReceived")?.value) || 0,
    };

    // Valider nødvendige felter
    if (!formData.name || !formData.description) {
        resultArea.style.color = "red";
        resultArea.textContent = "⚠️ Name and Description are required.";
        return;
    }

    try {
        const token = localStorage.getItem("access_token");
        if (!token) {
            throw new Error("❌ Authentication error: No token found!");
        }

        // Hent virksomhedens ID
        formData.company_id = await getCompanyId();

        // Vis en loading-tekst
        resultArea.style.color = "blue";
        resultArea.textContent = "⏳ Creating startup... Please wait.";

        // Send request til backend
        const response = await fetch("/startups/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const errMsg = await response.json();
            throw new Error(`Error: ${response.status}, ${errMsg.detail || "No detail provided"}`);
        }

        const data = await response.json();
        console.log("✅ Startup successfully created:", data);

        resultArea.style.color = "green";
        resultArea.textContent = `✅ Startup "${formData.name}" created successfully!`;

        // Ryd felterne efter succes
        startupForm.reset();

    } catch (error) {
        resultArea.style.color = "red";
        resultArea.textContent = `❌ Failed to create startup: ${error.message}`;
        console.error("Error:", error);
    }
}

// 🔹 Event listener til oprettelse af startup
startupForm.addEventListener("submit", createStartup);
