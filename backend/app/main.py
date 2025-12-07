from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from backend.app.routers.auth import router as auth_router
from backend.app.routers.calculation import router as calculation_router
from backend.app import database

# Create the FastAPI instance first
app = FastAPI(title="JWT Auth Example")

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(calculation_router, prefix="/calculations", tags=["calculations"])

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Startup event to initialize database
@app.on_event("startup")
def on_startup():
    database.init_db()

# Health endpoint
@app.api_route("/health", methods=["GET", "HEAD"])
def health():
    return {"status": "ok"}

# Validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"message": "Validation error", "details": exc.errors()}
    )

# Mount frontend static files if directory exists
ROOT_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = ROOT_DIR / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
