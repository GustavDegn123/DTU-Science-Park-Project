
# DTU Science Park Project

Et digitalt system designet til at forbedre matchmaking-processen mellem startups og investorer i DTU Science Park. Applikationen understøtter oprettelse og styring af profiler, forbindelser og investeringer, og kombinerer backend-logik med en enkel frontend.

## 🚀 Funktioner

- FastAPI-baseret webapplikation
- REST API til Startups, Investorer, Matches og Investments
- Autentificering og autorisation
- Databaseintegration via SQLAlchemy
- Klar til deployment og skalering
- Separat frontend (hostet i `/frontend`-mappen)

## 🧱 Teknologier

- **Backend:** FastAPI + Pydantic + SQLAlchemy
- **Database:** PostgreSQL
- **Frontend:** HTML/CSS/JS (kan opdateres med React eller andet)
- **Autentificering:** JWT-baseret login
- **Miljøstyring:** `.env`-fil og `python-dotenv`

## 📦 Installation (lokalt)

1. **Klon projektet:**
```bash
git clone https://github.com/GustavDegn123/DTU-Science-Park-Project.git
cd DTU-Science-Park-Project
```

2. **Opret og aktiver et virtuelt miljø:**
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

3. **Installer afhængigheder:**
```bash
pip install -r requirements.txt
```

4. **Kør applikationen:**
```bash
uvicorn main:app --reload
```

5. **Åbn i browseren:**
```text
http://127.0.0.1:8000
```
