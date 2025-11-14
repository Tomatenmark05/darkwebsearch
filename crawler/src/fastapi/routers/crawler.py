from fastapi import APIRouter, HTTPException
from schemas import CrawlRequest

router = APIRouter()

@router.post("/crawl")
async def start_crawl(request: CrawlRequest):
    addresses = request.addresses

    if not addresses or len(addresses) == 0:
        raise HTTPException(status_code=400, detail="No addresses provided")

    # Process addresses here
    return {"received_addresses": addresses}

@router.get("/status/{crawl_id}")
async def get_crawl_status(crawl_id: str):
    # Dummy implementation for crawl status retrieval
    dummy_status = {
        "crawl_id": crawl_id,
        "status": "in_progress",
    }
    return dummy_status

@router.get("/status") # used for a list of statuses
async def get_single_crawl_status():
    dummy_data = [
        {"jobId": "job-123", "status": "running"},
        {"jobId": "job-456", "status": "completed"},
        {"jobId": "job-789", "status": "failed"},
    ]
    return dummy_data