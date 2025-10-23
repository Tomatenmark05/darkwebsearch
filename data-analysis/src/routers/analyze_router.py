from fastapi import APIRouter, HTTPException

analyze_router = APIRouter()

@analyze_router.get("/status")
async def get_status():
    return {"status": "Analyzer is running"}
