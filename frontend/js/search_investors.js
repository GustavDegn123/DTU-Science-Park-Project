document.addEventListener("DOMContentLoaded", function () {
    const searchForm = document.getElementById("searchForm");
    const resultsContainer = document.getElementById("resultsContainer");
    const token = localStorage.getItem("access_token");

    searchForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const formData = new FormData(searchForm);
        const params = new URLSearchParams(formData).toString();
        const response = await fetch(`/investors/search?${params}`, {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            resultsContainer.innerHTML = "<p>❌ Error fetching results.</p>";
            return;
        }

        const investors = await response.json();
        resultsContainer.innerHTML = "";

        if (investors.length === 0) {
            resultsContainer.innerHTML = "<p>No matching investors found.</p>";
            return;
        }

        investors.forEach(investor => {
            const div = document.createElement("div");
            div.classList.add("investor-card");
            div.innerHTML = `
                <h2>${investor.firstname || "N/A"} ${investor.lastname || ""}</h2>
                <p><b>Sector:</b> ${investor.preferred_sectors || "N/A"}</p>
                <p><b>Impact Focus:</b> ${investor.impact_focus || "N/A"}</p>
                <p><b>Risk Profile:</b> ${investor.risk_profile || "N/A"}</p>
                <p><b>Minimum Investment:</b> ${investor.investment_range_min ? investor.investment_range_min.toLocaleString() + " DKK" : "N/A"}</p>
                <button class="match-btn" data-investor-id="${investor.investor_id}">Match</button>
            `;
            resultsContainer.appendChild(div);
        });

        document.querySelectorAll(".match-btn").forEach(button => {
            button.addEventListener("click", async function () {
                const investorId = this.getAttribute("data-investor-id");
                const startupId = 5; // 🔥 Hardcoded midlertidigt, du kan hente fra login

                const matchResponse = await fetch("/matchmaking/match-investor", {
                    method: "POST",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ 
                        investor_id: investorId, 
                        startup_id: startupId,  // ✅ Tilføj startup_id
                        match_score: 90, 
                        status: "Pending" 
                    })
                });

                if (matchResponse.ok) {
                    this.innerText = "Matched ✅";
                    this.disabled = true;
                } else {
                    alert("Error matching investor.");
                }
            });
        });
    });
});
