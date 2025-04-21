from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routes.auth import auth_router, get_current_user
from routes import investments, matchmaking, investors, companies, startups, investor_profiles
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db

app = FastAPI()

# ✅ Server statiske filer til frontend uden cache
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# ✅ Inkluder routere
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(investments.router, prefix="/investments", tags=["Investments"])
app.include_router(matchmaking.router, prefix="/matchmaking", tags=["Matchmaking"])
app.include_router(investors.router, prefix="/investors", tags=["Investors"])
app.include_router(companies.router, prefix="/companies", tags=["Companies"])
app.include_router(startups.router, prefix="/startups", tags=["Startups"])
app.include_router(investor_profiles.router, prefix="/investor_profiles", tags=["Investor Profiles"])


# ✅ Funktion til at returnere en fil med no-cache headers
def serve_file_nocache(filepath: str):
    response = FileResponse(filepath)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# ✅ Routes til frontend sider
@app.get("/about")
def serve_index():
    return serve_file_nocache("frontend/index.html")

@app.get("/login")
def login_page():
    return serve_file_nocache("frontend/login.html")

@app.get("/signup")
def signup_page():
    return serve_file_nocache("frontend/signup.html")

@app.get("/dashboard")
async def dashboard_redirect(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if hasattr(current_user, "business_email"):  # Hvis det er en virksomhed
        return serve_file_nocache("frontend/dashboard_company.html")
    else:
        return serve_file_nocache("frontend/dashboard_investor.html")

@app.get("/dashboard_company")
def dashboard_company():
    return serve_file_nocache("frontend/dashboard_company.html")

@app.get("/dashboard_investor")
def dashboard_investor():
    return serve_file_nocache("frontend/dashboard_investor.html")

@app.get("/investor_profile")
def investor_profile_page():
    return serve_file_nocache("frontend/investor_profile.html")

@app.get("/add-startup")
def add_startup_page():
    return serve_file_nocache("frontend/add-startup.html")

@app.get("/search_startups")
def search_startups_page():
    return serve_file_nocache("frontend/search_startups.html")

@app.get("/my_matches")  # Ændret fra "/my-matches" til "/my_matches"
def my_matches_page():
    return serve_file_nocache("frontend/my_matches.html")

@app.get("/search_investors")
def search_investors_page():
    return serve_file_nocache("frontend/search_investors.html")

@app.get("/my_startup_matches")
def my_startup_matches_page():
    return serve_file_nocache("frontend/my_startup_matches.html")

# ✅ Server statiske JS-filer med no-cache
@app.get("/frontend/js/{filename}")
def serve_js_files(filename: str):
    return serve_file_nocache(f"frontend/js/{filename}")

# ✅ Server statiske CSS-filer med no-cache
@app.get("/frontend/css/{filename}")
def serve_css_files(filename: str):
    return serve_file_nocache(f"frontend/css/{filename}")

import logging


