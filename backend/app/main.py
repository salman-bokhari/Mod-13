from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

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
# Exception handlers
# ------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    # Combine all errors into a single string message
    messages = []
    for e in exc.errors():
        loc = ".".join(str(x) for x in e['loc'] if isinstance(x, str))
        msg = e['msg']
        messages.append(f"{loc}: {msg}")
    # Return a single 'detail' that Playwright expects
    return JSONResponse(
        status_code=400,
        content={"detail": "Error during registration", "errors": messages}
    )

    
# ------------------------
# Serve frontend correctly
# ------------------------
ROOT_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = ROOT_DIR / "frontend"

if FRONTEND_DIR.exists():
    # Serve frontend at root so fetch('/register') works correctly
    app.mount(
        "/",
        StaticFiles(directory=str(FRONTEND_DIR), html=True),
        name="frontend"
    )
else:
    print("⚠️ Frontend directory NOT found:", FRONTEND_DIR)
