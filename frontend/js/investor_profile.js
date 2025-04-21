document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
        console.error("❌ No token found! Redirecting to login...");
        window.location.href = "/login";
        return;
    }

    try {
        const profile = await getInvestorProfile(token);
        if (profile) {
            console.log("✅ Profile found, populating form...");
            populateForm(profile);
        } else {
            console.warn("⚠️ No investor profile found. User must create one manually.");
        }
    } catch (error) {
        console.error("❌ Error handling investor profile:", error);
    }
});

// ✅ Henter investorprofil
async function getInvestorProfile(token) {
    try {
        const response = await fetch("/investor_profiles/", {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (response.ok) return await response.json();
        if (response.status === 404) return null; // Ingen profil fundet
        throw new Error(`Failed to fetch investor profile: ${response.status}`);
    } catch (error) {
        console.error("❌ Error fetching profile:", error);
        return null;
    }
}

// ✅ Opretter eller opdaterer investorprofil afhængigt af om en profil findes
document.getElementById("saveProfileButton").addEventListener("click", async (event) => {
    event.preventDefault(); // Forhindrer siden i at reloade

    const token = localStorage.getItem("access_token");
    if (!token) {
        console.error("❌ No token found! Redirecting to login...");
        window.location.href = "/login";
        return;
    }

    try {
        // Hent investor_id fra backend, da det kræves for at oprette profilen
        const userResponse = await fetch("/auth/user", {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (!userResponse.ok) {
            throw new Error("❌ Failed to fetch user data");
        }

        const userData = await userResponse.json();
        const investorId = userData.id;  // Henter investor_id fra user-data

        const profile = await getInvestorProfile(token); // Tjek om en profil allerede findes

        const profileData = {
            investor_id: investorId, // ✅ Tilføjer investor_id
            investor_type: document.querySelector("[name='investorType']").value,
            preferred_sectors: document.querySelector("[name='preferredSectors']").value,
            impact_focus: document.querySelector("[name='impactFocus']").value,
            investment_range_min: parseFloat(document.querySelector("[name='investmentMin']").value) || null,
            investment_range_max: parseFloat(document.querySelector("[name='investmentMax']").value) || null,
            risk_profile: document.querySelector("[name='riskProfile']").value,
            preferred_esg_score: parseFloat(document.querySelector("[name='esgScore']").value) || null
        };

        if (profile) {
            await updateInvestorProfile(token, profileData);
        } else {
            await createInvestorProfile(token, profileData);
        }

    } catch (error) {
        console.error("❌ Error handling profile:", error);
        alert("Error processing profile. Please try again.");
    }
});

// ✅ Opretter en investorprofil
async function createInvestorProfile(token, profileData) {
    try {
        const response = await fetch("/investor_profiles/", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(profileData)
        });

        if (response.ok) {
            console.log("✅ Investor profile created successfully.");
            alert("Profile created successfully!");
        } else {
            const errorData = await response.json();
            throw new Error(`❌ Failed to create investor profile: ${errorData.detail || "Unknown error"}`);
        }
    } catch (error) {
        console.error("❌ Error creating profile:", error);
        alert("Error creating profile. Please try again.");
    }
}

// ✅ Opdaterer en eksisterende investorprofil
async function updateInvestorProfile(token, profileData) {
    try {
        const response = await fetch("/investor_profiles/", {
            method: "PUT",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(profileData)
        });

        if (response.ok) {
            console.log("✅ Investor profile updated successfully.");
            alert("Profile updated successfully!");
        } else {
            const errorData = await response.json();
            throw new Error(`❌ Failed to update investor profile: ${errorData.detail || "Unknown error"}`);
        }
    } catch (error) {
        console.error("❌ Error updating profile:", error);
        alert("Error updating profile. Please try again.");
    }
}

// ✅ Fylder HTML-formularen med investorens data
function populateForm(profile) {
    document.querySelector("[name='investorType']").value = profile.investor_type || "";
    document.querySelector("[name='preferredSectors']").value = profile.preferred_sectors || "";
    document.querySelector("[name='impactFocus']").value = profile.impact_focus || "";
    document.querySelector("[name='investmentMin']").value = profile.investment_range_min || "";
    document.querySelector("[name='investmentMax']").value = profile.investment_range_max || "";
    document.querySelector("[name='riskProfile']").value = profile.risk_profile || "Low";
    document.querySelector("[name='esgScore']").value = profile.preferred_esg_score || "";
}
