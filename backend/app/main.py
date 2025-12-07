from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from backend.app.routers import auth as auth_router
from backend.app import database

app = FastAPI(title="JWT Auth Example")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.on_event("startup")
def on_startup():
    database.init_db()

@app.api_route("/health", methods=["GET", "HEAD"])
def health():
    return {"status": "ok"}

app.include_router(auth_router.router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"message": "Error during registration"}
    )

ROOT_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = ROOT_DIR / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
