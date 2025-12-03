from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from backend.app.routers import auth as auth_router
from backend.app import database

app = FastAPI(title="JWT Auth Example")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# DB startup
@app.on_event("startup")
def on_startup():
    database.init_db()

# Health check
@app.api_route("/health", methods=["GET", "HEAD"])
def health():
    return {"status": "ok"}


# Include API router **before** static files
app.include_router(auth_router.router)

# Serve frontend
ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIR = ROOT / "frontend"

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
