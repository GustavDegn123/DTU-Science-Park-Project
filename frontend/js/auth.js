console.log("auth.js loaded.");

const token = localStorage.getItem("access_token");
const userRole = localStorage.getItem("user_type");

const navMenu = document.querySelector(".nav-menu"); // 🔥 Sørg for, at navMenu er defineret

function updateNavMenu() {
    if (!navMenu) {
        console.error("❌ navMenu element not found!");
        return;
    }

    navMenu.innerHTML = "";

    if (!token) {
        navMenu.innerHTML += `<li><a href="/about">About</a></li>`;
        navMenu.innerHTML += `<li><a href="/login">Login</a></li>`;
        navMenu.innerHTML += `<li><a href="/signup">Sign Up</a></li>`;
    } else {
        const dashboardLink = `<li><a href="${userRole === "company" ? "/dashboard_company" : "/dashboard_investor"}" class="active">Dashboard</a></li>`;
        navMenu.innerHTML += dashboardLink;

        if (userRole === "company") {
            navMenu.innerHTML += `<li><a href="/add-startup">Add Startup</a></li>`;
            navMenu.innerHTML += `<li><a href="/search_investors">Find Investors</a></li>`; 
            navMenu.innerHTML += `<li><a href="/my_startup_matches">My Matches</a></li>`; //
        } else {
            navMenu.innerHTML += `<li><a href="/search_startups">Search Startups</a></li>`;
            navMenu.innerHTML += `<li><a href="/my_matches">My Matches</a></li>`;
        }

        const logoutLink = document.createElement("li");
        logoutLink.innerHTML = `<a href="#">Log out</a>`;
        logoutLink.addEventListener("click", () => {
            localStorage.clear();
            window.location.href = "/login";
        });
        navMenu.appendChild(logoutLink);
    }
}

// Kald funktionen for at opdatere navigationen
updateNavMenu();
