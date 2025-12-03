from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from backend.app.routers import auth as auth_router
from backend.app import database

app = FastAPI(title="JWT Auth Example")

# ------------------------
# CORS
# ------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# ------------------------
# DB startup
# ------------------------
@app.on_event("startup")
def on_startup():
    database.init_db()

# ------------------------
# Health check
# ------------------------
@app.api_route("/health", methods=["GET", "HEAD"])
def health():
    return {"status": "ok"}

# ------------------------
# API routers
# ------------------------
app.include_router(auth_router.router)

# ------------------------
# Serve frontend correctly
# ------------------------
# backend/app/main.py → parents[1] = backend/
#                      → parents[2] = project root
ROOT_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = ROOT_DIR / "frontend"

if FRONTEND_DIR.exists():
    # Mount frontend as /frontend
    app.mount(
        "/frontend",
        StaticFiles(directory=str(FRONTEND_DIR), html=True),
        name="frontend"
    )
else:
    print("⚠️ Frontend directory NOT found:", FRONTEND_DIR)
