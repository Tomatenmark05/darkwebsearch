from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import search

app = FastAPI(
    title="Darkwebsearch - GUI API",
    version="1.0.0",
    description="API for dark web search interface",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://sveltekitgui:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, tags=["Search"])

@app.get("/")
async def root():
    return {"message": "Darkwebsearch API is running"}