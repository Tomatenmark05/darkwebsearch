import os
import uuid
import time
import hmac
import hashlib
import json
import asyncio
from typing import Dict, Any

import requests
from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from models import AnalyzeRequest, JobAccepted, AnalysisResult
from ai_client import analyze_content_sync

analyze_router = APIRouter()
security = HTTPBearer()

API_KEY = os.getenv("API_KEY", "changeme")
DEFAULT_CALLBACK_URL = os.getenv("CALLBACK_URL")  # e.g. https://external.example.com/result
SHARED_SECRET = os.getenv("SHARED_SECRET")  # optional HMAC signing secret
DELIVERY_MAX_RETRIES = int(os.getenv("DELIVERY_MAX_RETRIES", "3"))
DELIVERY_INITIAL_DELAY = float(os.getenv("DELIVERY_INITIAL_DELAY", "1.0"))
DELIVERY_BACKOFF_FACTOR = float(os.getenv("DELIVERY_BACKOFF_FACTOR", "2.0"))
HTTP_TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "10.0"))

# In-memory job store: jobId -> state dict
JOB_STORE: Dict[str, Dict[str, Any]] = {}


def require_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    token = credentials.credentials
    if token != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")
    return token


def deliver_result(result: AnalysisResult, callback_url: str) -> bool:
    """
    Synchronously deliver the analysis result using requests with retries.
    Adds optional HMAC signature header if SHARED_SECRET set.
    """
    payload = result.model_dump()
    body = json.dumps(payload)
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {API_KEY}"} 

    if SHARED_SECRET:
        signature = hmac.new(
            SHARED_SECRET.encode("utf-8"),
            body.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        headers["X-Signature"] = signature

    delay = DELIVERY_INITIAL_DELAY
    attempt = 0
    while attempt < DELIVERY_MAX_RETRIES:
        attempt += 1
        try:
            resp = requests.post(callback_url, data=body, headers=headers, timeout=HTTP_TIMEOUT)
            if 200 <= resp.status_code < 300:
                return True
            else:
                print(f"[deliver_result] Attempt {attempt}: Non-success {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"[deliver_result] Attempt {attempt}: Exception - {e}")

        if attempt < DELIVERY_MAX_RETRIES:
            time.sleep(delay)
            delay *= DELIVERY_BACKOFF_FACTOR

    return False


def process_job(job_id: str, content: str, callback_url: str):
    """
    Perform analysis (potentially blocking) and deliver results.
    """
    try:
        # Use to_thread for potential heavy model call (optional)
        analysis_dict = asyncio.run(asyncio.to_thread(analyze_content_sync, content))
        result = AnalysisResult(**{**analysis_dict, "jobId": job_id})
        JOB_STORE[job_id]["result"] = result
        JOB_STORE[job_id]["done"] = True

        delivered = deliver_result(result, callback_url)
        if delivered:
            JOB_STORE[job_id]["delivered"] = True
        else:
            JOB_STORE[job_id]["deliveryFailed"] = True

    except Exception as exc:
        print(f"[process_job] Job {job_id} failed: {exc}")
        JOB_STORE[job_id]["error"] = str(exc)
        JOB_STORE[job_id]["done"] = True


@analyze_router.post("/analyze", response_model=JobAccepted, status_code=status.HTTP_202_ACCEPTED)
def analyze_data(payload: AnalyzeRequest, background: BackgroundTasks, api_key: str = Depends(require_api_key)):
    """
    Queue an analysis job. Returns only jobId immediately.
    Result will be POSTed to callbackUrl.
    """
    if not payload.content or not payload.content.strip():
        raise HTTPException(status_code=400, detail="No data provided for analysis")

    callback_url = payload.callbackUrl or DEFAULT_CALLBACK_URL
    if not callback_url:
        raise HTTPException(status_code=400, detail="No callback URL provided (missing callbackUrl field or CALLBACK_URL env var)")

    job_id = str(uuid.uuid4())
    JOB_STORE[job_id] = {
        "done": False,
        "result": None,
        "callbackUrl": callback_url,
        "delivered": False
    }

    # Schedule synchronous processing (runs after response is returned)
    background.add_task(process_job, job_id, payload.content, callback_url)

    return JobAccepted(jobId=job_id)


@analyze_router.get("/status")
def get_status(jobId: str = Query(..., alias="jobId"), api_key: str = Depends(require_api_key)):
    """
    Return True if analysis finished (regardless of delivery success), False otherwise.
    """
    job = JOB_STORE.get(jobId)
    if job is None:
        raise HTTPException(status_code=400, detail="Unknown jobId")
    return job.get("done", False)
