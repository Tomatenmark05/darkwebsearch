from fastapi import APIRouter, HTTPException

status_router = APIRouter()

@status_router.get("/status")
async def get_status():
    return {"status": "Status is running"}

