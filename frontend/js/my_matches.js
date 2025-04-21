document.addEventListener("DOMContentLoaded", async function () {
    const matchesContainer = document.getElementById("matchesContainer");
    const token = localStorage.getItem("access_token");

    if (!token) {
        matchesContainer.innerHTML = "<p>❌ Please log in to see your matches.</p>";
        return;
    }

    const response = await fetch("/matchmaking/my-matches", {
        headers: { "Authorization": `Bearer ${token}` }
    });

    if (!response.ok) {
        matchesContainer.innerHTML = "<p>❌ Error fetching matches.</p>";
        return;
    }

    const startups = await response.json();
    if (startups.length === 0) {
        matchesContainer.innerHTML = "<p>No matched startups found.</p>";
        return;
    }

    startups.forEach(startup => {
        const div = document.createElement("div");
        div.classList.add("startup-card");
    
        div.innerHTML = `
            <h2>${startup.name}</h2>
            <p><b>Sector:</b> ${startup.sector || "N/A"}</p>
            <p><b>Funding Stage:</b> ${startup.funding_stage || "N/A"}</p>
            <p><b>Revenue:</b> ${startup.revenue ? startup.revenue.toLocaleString() + " DKK" : "N/A"}</p>
            <p><b>Employees:</b> ${startup.employees || "N/A"}</p>
        `;
    
        matchesContainer.appendChild(div);
    });    
});
