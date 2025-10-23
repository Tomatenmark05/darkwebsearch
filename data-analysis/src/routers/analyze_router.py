from fastapi import APIRouter, HTTPException
import models as models

analyze_router = APIRouter()

@analyze_router.get("/status")
async def get_status():
    return {"status": "Analyzer is running"}

@analyze_router.post("/")
async def analyze_data(data: models.Content):
    if not data:
        raise HTTPException(status_code=400, detail="No data provided for analysis")

    analysis_result = {"summary": "This is a mock analysis result."}
    return {"data": data, "analysis": analysis_result}
