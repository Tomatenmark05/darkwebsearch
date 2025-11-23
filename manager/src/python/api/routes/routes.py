from typing import List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, status, BackgroundTasks
from pydantic import BaseModel
from api.db.models import ContentTag, Tag, Content
from api.db.database import get_db
from sqlalchemy.orm import Session, joinedload

from continous_loop import loop

router = APIRouter()


class SearchRequest(BaseModel):
    query: str


class SearchResult(BaseModel):
    title: Optional[str]
    url: Optional[str]
    description: Optional[str]


class CrawlItem(BaseModel):
    url: str
    content: str
    metadata: Optional[dict] = None


class CrawlRequest(BaseModel):
    results: List[CrawlItem]


class AnalyseItem(BaseModel):
    jobId: Optional[str]
    title: Optional[str]
    description: Optional[str]
    url: Optional[str]
    tags: Optional[List[str]] = None
    legality: Optional[bool] = None


class AnalyseRequest(BaseModel):
    results: List[AnalyseItem]


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


def _require_apikey(authorization: Optional[str] = Header(None)) -> str:
    """Placeholder API key auth dependency.

    In production, validate the API key against the DB and enforce scopes/rate limits.
    """
    return _require_jwt(authorization)


@router.post("/search")
async def search(req: SearchRequest, token: str = Depends(_require_jwt), session: Session = Depends(get_db)):
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
    return SearchResponse(results=results)


@router.post("/crawl-results")
async def crawl_results(req: CrawlRequest, apikey: str = Depends(_require_apikey)) -> bool:
    """Accept crawled data from crawler services. (placeholder)

    TODO: validate payload, persist crawl results, create analysis jobs.
    """
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="crawl-results not implemented yet")


@router.post("/analyze-results")
async def analyse_results(req: AnalyseRequest, apikey: str = Depends(_require_apikey)) -> bool:
    """Accept analysis results. (placeholder)

    TODO: validate payload, persist analysis results, update indices.
    """
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="analyse-results not implemented yet")

@router.post("/start-loop")
async def start_loop(background: BackgroundTasks):
    loop.active = True
    background.add_task(loop.continious_loop)
    return 200

@router.post("/stop-loop")
async def stop_loop():
    loop.active = False
    return 200








