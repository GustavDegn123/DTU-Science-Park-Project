document.addEventListener("DOMContentLoaded", () => {
    const investorBtn = document.getElementById("investorBtn");
    const companyBtn = document.getElementById("companyBtn");
    const investorFields = document.getElementById("investorFields");
    const companyFields = document.getElementById("companyFields");
    const signupForm = document.getElementById("signupForm");

    function toggleFields(role) {
        if (role === "investor") {
            investorFields.style.display = "block";
            companyFields.style.display = "none";
            investorBtn.classList.add("active");
            companyBtn.classList.remove("active");

            // Aktiver kun investor-felter
            Array.from(investorFields.querySelectorAll("input")).forEach(input => input.removeAttribute("disabled"));
            Array.from(companyFields.querySelectorAll("input")).forEach(input => input.setAttribute("disabled", "true"));
        } else {
            investorFields.style.display = "none";
            companyFields.style.display = "block";
            companyBtn.classList.add("active");
            investorBtn.classList.remove("active");

            // Aktiver kun company-felter
            Array.from(companyFields.querySelectorAll("input")).forEach(input => input.removeAttribute("disabled"));
            Array.from(investorFields.querySelectorAll("input")).forEach(input => input.setAttribute("disabled", "true"));
        }
    }

    investorBtn.addEventListener("click", () => toggleFields("investor"));
    companyBtn.addEventListener("click", () => toggleFields("company"));

    signupForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        let payload = {};
        let url = "";

        if (companyBtn.classList.contains("active")) {
            payload = {
                name: document.getElementById("companyName").value.trim(),
                business_email: document.getElementById("companyEmail").value.trim(),
                password: document.getElementById("companyPassword").value.trim(),
                firstname: document.getElementById("companyFirstname").value.trim(),
                lastname: document.getElementById("companyLastname").value.trim(),
                country: document.getElementById("companyCountry").value.trim(),
            };
            url = "/auth/signup/company";
        } else {
            payload = {
                name: document.getElementById("investorName").value.trim(),
                email: document.getElementById("investorEmail").value.trim(),
                password: document.getElementById("investorPassword").value.trim(),
                firstname: document.getElementById("investorFirstname").value.trim(),
                lastname: document.getElementById("investorLastname").value.trim(),
                country: document.getElementById("investorCountry").value.trim(),
            };
            url = "/auth/signup/investor";
        }

        try {
            const response = await fetch(url, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });

            const result = await response.json();
            if (!response.ok) {
                throw new Error(result.detail || "Signup failed");
            }

            alert("Account created successfully!");
            window.location.href = "/login";
        } catch (error) {
            alert(error.message);
        }
    });

    toggleFields("investor");
});
