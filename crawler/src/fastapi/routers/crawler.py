from fastapi import APIRouter, HTTPException, status
from schemas import CrawlRequest
from  crawler import Crawler, JOB_STORE

router = APIRouter()

@router.post("/crawl")
async def start_crawl(request: CrawlRequest):
    addresses = request.addresses

    if not addresses or len(addresses) == 0:
        raise HTTPException(status_code=400, detail="No addresses provided")

    crawler = Crawler()
    job_id = crawler.start_crawl(addresses)

    return {"job_id": job_id}

@router.get("/status/{job_id}")
async def get_crawl_status(job_id: str):
    job = Crawler.get_job(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    return {
        'job_id': job_id,
        'status': job.get('status'),
        'created_at': job.get('created_at'),
        'finished_at': job.get('finished_at'),
        'analysis_status': job.get('analysis_status')
    }


@router.get("/status")
async def list_crawl_statuses():
    return [{ 'job_id': jid, 'status': j.get('status') } for jid, j in JOB_STORE.items()]