import os
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx

logger = logging.getLogger("sveltgui.analyze")

DOWNSTREAM_URL = os.getenv("DOWNSTREAM_URL", "").strip()
DOWNSTREAM_SEARCH_PATH = "/search"  # adjust if downstream expects a different route

analyze_router = APIRouter()

class AnalyzeRequest(BaseModel):
    query: str

class AnalyzeResponse(BaseModel):
    status: str
    query: str
    forwarded: bool
    downstream_status: Optional[int] = None
    downstream_error: Optional[str] = None
    downstream_response: Optional[dict] = None

@analyze_router.post("/search", response_model=AnalyzeResponse)
async def analyze_search(req: AnalyzeRequest):
    """Receive a query and optionally forward to downstream microservice."""
    q = req.query.strip()
    if not q:
        raise HTTPException(status_code=400, detail="Empty query")

    logger.info(f"Received analyze query: {q}")

    if not DOWNSTREAM_URL:
        return AnalyzeResponse(
            status="received",
            query=q,
            forwarded=False
        )

    url = f"{DOWNSTREAM_URL.rstrip('/')}{DOWNSTREAM_SEARCH_PATH}"
    logger.debug(f"Forwarding to downstream: {url}")

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            resp = await client.post(url, json={"query": q})
            content_type = resp.headers.get("content-type", "")
            if "application/json" in content_type:
                downstream_json = resp.json()
            else:
                downstream_json = {"raw": resp.text}

            return AnalyzeResponse(
                status="received",
                query=q,
                forwarded=True,
                downstream_status=resp.status_code,
                downstream_error=None if resp.status_code < 400 else resp.text,
                downstream_response=downstream_json
            )
        except httpx.RequestError as e:
            logger.error(f"Downstream request error: {e}")
            return AnalyzeResponse(
                status="received",
                query=q,
                forwarded=True,
                downstream_status=None,
                downstream_error=str(e),
                downstream_response=None
            )