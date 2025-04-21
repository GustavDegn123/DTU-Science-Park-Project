from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")  # Angiver stien til .env-fil, hvis nødvendigt

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL ikke fundet! Sørg for at have en .env-fil.")
