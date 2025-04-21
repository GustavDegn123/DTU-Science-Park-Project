document.addEventListener("DOMContentLoaded", function () {
    const searchForm = document.getElementById("searchForm");
    const resultsContainer = document.getElementById("resultsContainer");

    searchForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const formData = new FormData(searchForm);
        const params = new URLSearchParams(formData).toString();
        const response = await fetch(`/matchmaking/search-startups?${params}`);

        if (!response.ok) {
            resultsContainer.innerHTML = "<p>❌ Error fetching results.</p>";
            return;
        }

        const startups = await response.json();
        resultsContainer.innerHTML = "";

        if (startups.length === 0) {
            resultsContainer.innerHTML = "<p>No matching startups found.</p>";
            return;
        }

        startups.forEach((s) => {
            const div = document.createElement("div");
            div.classList.add("startup-card");
            div.innerHTML = `
                <h3>${s.name}</h3>
                <p><b>Sector:</b> ${s.sector || "N/A"}</p>
                <p><b>Funding Stage:</b> ${s.funding_stage || "N/A"}</p>
                <p><b>Revenue:</b> ${s.revenue ? s.revenue.toLocaleString() + " DKK" : "N/A"}</p>
                <p><b>Employees:</b> ${s.employees || "N/A"}</p>
                <p><b>ESG Score:</b> ${s.esg_score || "N/A"}</p>
                <p><b>Traction Score:</b> ${s.traction || "N/A"}</p>
                <button class="save-match" data-id="${s.id}" style="background-color: #990000; color: white; border: none; padding: 10px; border-radius: 8px; cursor: pointer; font-size: 1rem; width: 100%; font-weight: bold;">Save Match</button>
            `;
            resultsContainer.appendChild(div);
        });

        document.querySelectorAll(".save-match").forEach(button => {
            button.addEventListener("click", async function () {
                const startupId = this.dataset.id;
                const token = localStorage.getItem("access_token"); 

                if (!token) {
                    alert("❌ No token found. Please log in.");
                    return;
                }

                const response = await fetch(`/matchmaking/`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`
                    },
                    body: JSON.stringify({ 
                        startup_id: startupId,  // 🚀 Ingen investor_id
                        match_score: 95.0, 
                        status: "Accepted"
                    })
                });                

                if (response.ok) {
                    this.innerText = "Accepted";
                    this.style.backgroundColor = "#990000"; 
                    this.style.cursor = "default";
                    this.disabled = true;
                } else {
                    alert("❌ Error saving match");
                }
            });
        });
    });
});
