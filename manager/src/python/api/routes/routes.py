from typing import List, Optional

import os
from fastapi import APIRouter, Depends, Header, HTTPException, status, BackgroundTasks
from pydantic import BaseModel
from api.db.models import ContentTag, Tag, Content, Links
from api.db.database import get_db
from sqlalchemy.orm import Session, joinedload
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import datetime

from continous_loop import loop

router = APIRouter()

API_KEY = os.getenv("API_KEY", "changeme")
security = HTTPBearer()

class SearchResult(BaseModel):
    title: Optional[str]
    url: Optional[str]
    description: Optional[str]

class CrawlResult(BaseModel):
    url: str
    job_id: str
    content: str

class AnalyseResult(BaseModel):
    jobId: Optional[str]
    title: Optional[str]
    legality: Optional[bool] = None
    description: Optional[str]
    url: Optional[str]
    tags: Optional[List[str]] = None

class SearchRequest(BaseModel):
    query: str
    user: dict



def _require_jwt(authorization: Optional[str] = Header(None)) -> str:
    """Placeholder JWT auth dependency.

    Replace with proper JWT verification (signature, claims, expiry) before using in prod.
    """
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
    parts = authorization.split(None, 1)
    if len(parts) != 2 or parts[0].lower() != "bearer" or not parts[1].strip():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header")
    return parts[1].strip()


def require_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    token = credentials.credentials
    if token != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")
    return token


@router.post("/search")
async def search(req: SearchRequest, session: Session = Depends(get_db)):
    # exact match on tag name; use .ilike(f"%{req.query}%") for substring/case-insensitive
    q = (
        session.query(Content)
        .join(ContentTag)          # join association object
        .join(Tag)                 # join tag
        .filter(Tag.name.ilike(f"%{req.query}%"))  # filter by tag name
        .order_by(ContentTag.priority.desc())
        .distinct(Content.id)      # remove duplicate contents if multiple matching rows
        .options(joinedload(Content.tag_links).joinedload(ContentTag.tag))  # avoid N+1 when accessing tags
        .limit(100)
    )

    results = []
    for content in q.all():
        results.append(SearchResult(
            title=getattr(content, "title", None) or content.url,
            url=content.url,
            description=getattr(content, "description", "")
        ))
    print(results)
    return results


@router.post("/crawl-results")
async def crawl_results(req: CrawlResult, db: Session = Depends(get_db)) -> bool:
    if req.job_id and req.content:
        url = loop.crawler_running_jobs[req.job_id]

        link = db.query(Links).filter(Links.url == url).first()
        link.analysed_on = datetime.date.today()
        db.commit()

        loop.crawler_running_jobs.pop(req.job_id)

        status = loop.start_analysejob(req.content, url)

    if status:
        return True
    else:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="crawl-results not implemented yet")



@router.post("/analyze-results")
async def analyse_results(req: AnalyseResult, db: Session = Depends(get_db)) -> bool:

    if not req.tags:
        required_tags = []
    else:

        tag_names = set(req.tags)
        existing_tags = db.query(Tag).filter(Tag.name.in_(tag_names)).all()

        existing_names = {tag.name for tag in existing_tags}
        missing_names = tag_names - existing_names

        new_tags = [Tag(name=name) for name in missing_names]

        if new_tags:
            db.add_all(new_tags)

        required_tags = existing_tags + new_tags


    real_url = loop.analyse_running_jobs[req.jobId]
    loop.analyse_running_jobs.pop(req.jobId)
    new_content = Content(
        url = real_url,
        title = req.title,
        description = req.description,
        tag_links = [ContentTag(tag=tag) for tag in required_tags]
    )

    db.add(new_content)

    try:
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error saving content: {e}")
        return False



@router.post("/start-loop")
async def start_loop(background: BackgroundTasks):
    loop.active = True
    background.add_task(loop.continious_loop)
    return 200

@router.post("/stop-loop")
async def stop_loop():
    loop.active = False
    return 200








