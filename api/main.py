import uvicorn
from core.logging_config import setup_logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # <--- Importar esto
from fastapi.responses import FileResponse   # <--- Importar esto
from routers.honeytokens import router as honeytokens_router
from routers.static_files import router as static_files_router
import os

setup_logging()

app = FastAPI(
    title="Honeytokens Manager API",
    description="API designed for honeytokens management",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(honeytokens_router)
app.include_router(static_files_router)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/dashboard", tags=["System"])
async def read_dashboard():
    return FileResponse(os.path.join(STATIC_DIR, "dashboard.html"))

@app.get("/health", tags=["System"])
def healthcheck():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)