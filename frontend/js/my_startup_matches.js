document.addEventListener("DOMContentLoaded", async function () {
    const matchesContainer = document.getElementById("matchesContainer");
    const token = localStorage.getItem("access_token");

    if (!token) {
        matchesContainer.innerHTML = "<p>❌ Please log in to see your matches.</p>";
        return;
    }

    const response = await fetch("/matchmaking/my-matched-investors", {
        headers: { "Authorization": `Bearer ${token}` }
    });

    if (!response.ok) {
        matchesContainer.innerHTML = "<p>❌ Error fetching matches.</p>";
        return;
    }

    const investors = await response.json();
    
    // 🛠 Debug log for at se præcist hvad API'et returnerer
    console.log("API Response:", investors); 

    matchesContainer.innerHTML = investors.length === 0 ? "<p>No matched investors found.</p>" : "";

    investors.forEach(investor => {
        const div = document.createElement("div");
        div.classList.add("investor-card");
        div.innerHTML = `
            <h2>${investor.firstname} ${investor.lastname}</h2>
            <p><b>Sector:</b> ${investor.preferred_sectors || "N/A"}</p>
            <p><b>Investment Range:</b> ${investor.investment_range_min || "N/A"} - ${investor.investment_range_max || "N/A"} DKK</p>
            <p><b>Impact Focus:</b> ${investor.impact_focus || "N/A"}</p>
            <p><b>Risk Profile:</b> ${investor.risk_profile || "N/A"}</p>
        `;
        matchesContainer.appendChild(div);
    });
});
