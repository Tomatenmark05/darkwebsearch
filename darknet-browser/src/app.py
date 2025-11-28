import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from routers.analyze_router import analyze_router

LOG_LEVEL = os.getenv("LOG_LEVEL", "info").upper()
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger("sveltgui")

app = FastAPI(title="Svelte GUI Microservice", version="0.1.1")

# Mount built static assets (Svelte)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include analyze router
app.include_router(analyze_router, prefix="/analyze", tags=["analyze"])

# CORS (loose for prototype)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

# SPA fallback
@app.get("/{full_path:path}")
async def spa_fallback(full_path: str):
    index_file = "app/static/index.html"
    if os.path.isfile(index_file):
        return FileResponse(index_file)
    raise HTTPException(status_code=404, detail="Frontend not built")