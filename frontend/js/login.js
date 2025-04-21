document.addEventListener("DOMContentLoaded", () => {
    const investorLoginBtn = document.getElementById("investorLoginBtn");
    const companyLoginBtn = document.getElementById("companyLoginBtn");
    const investorLoginFields = document.getElementById("investorLoginFields");
    const companyLoginFields = document.getElementById("companyLoginFields");
    const loginForm = document.getElementById("loginForm");
    const loginResult = document.getElementById("loginResult");

    function toggleLoginFields(role) {
        if (role === "investor") {
            investorLoginFields.style.display = "block";
            companyLoginFields.style.display = "none";
            investorLoginBtn.classList.add("active");
            companyLoginBtn.classList.remove("active");

            // Aktiver kun investor-felter
            Array.from(investorLoginFields.querySelectorAll("input")).forEach(input => input.removeAttribute("disabled"));
            Array.from(companyLoginFields.querySelectorAll("input")).forEach(input => input.setAttribute("disabled", "true"));
        } else {
            investorLoginFields.style.display = "none";
            companyLoginFields.style.display = "block";
            companyLoginBtn.classList.add("active");
            investorLoginBtn.classList.remove("active");

            // Aktiver kun company-felter
            Array.from(companyLoginFields.querySelectorAll("input")).forEach(input => input.removeAttribute("disabled"));
            Array.from(investorLoginFields.querySelectorAll("input")).forEach(input => input.setAttribute("disabled", "true"));
        }
    }

    investorLoginBtn.addEventListener("click", () => toggleLoginFields("investor"));
    companyLoginBtn.addEventListener("click", () => toggleLoginFields("company"));

    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        let payload;
        let userType;

        if (companyLoginBtn.classList.contains("active")) {
            // ✅ Sørg for, at kun de synlige felter fra companyLoginFields bliver sendt
            payload = new URLSearchParams({
                username: document.getElementById("companyEmail").value.trim(),
                password: document.getElementById("companyPassword").value.trim(),
            });
            userType = "company";
        } else {
            // ✅ Sørg for, at kun de synlige felter fra investorLoginFields bliver sendt
            payload = new URLSearchParams({
                username: document.getElementById("investorEmail").value.trim(),
                password: document.getElementById("investorPassword").value.trim(),
            });
            userType = "investor";
        }

        try {
            const response = await fetch("/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: payload,
            });

            const result = await response.json();
            if (!response.ok) throw new Error(result.detail || "Login failed");

            localStorage.setItem("access_token", result.access_token);
            localStorage.setItem("user_type", userType);

            loginResult.textContent = "Login successful!";
            loginResult.style.color = "green";

            setTimeout(() => {
                window.location.href = userType === "company" ? "/dashboard_company" : "/dashboard_investor";
            }, 1000);
        } catch (error) {
            loginResult.textContent = error.message;
            loginResult.style.color = "red";
        }
    });

    toggleLoginFields("investor");
});
