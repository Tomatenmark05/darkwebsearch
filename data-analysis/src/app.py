from fastapi import FastAPI
from routers.analyze_router import analyze_router

app = FastAPI()

app.include_router(analyze_router,  tags=["analyze"])








