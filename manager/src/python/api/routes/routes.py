from typing import List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel

router = APIRouter()


class SearchRequest(BaseModel):
    query: str


class SearchResult(BaseModel):
    title: Optional[str]
    url: Optional[str]
    description: Optional[str]


class SearchResponse(BaseModel):
    results: List[SearchResult]


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


@router.post("/search", response_model=SearchResponse)
async def search(req: SearchRequest, token: str = Depends(_require_jwt)) -> SearchResponse:
    """Perform a search query. (placeholder)

    TODO: wire up search to DB / search index and return real results.
    """
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="search not implemented yet")


@router.post("/crawl-results")
async def crawl_results(req: CrawlRequest, apikey: str = Depends(_require_apikey)) -> bool:
    """Accept crawled data from crawler services. (placeholder)

    TODO: validate payload, persist crawl results, create analysis jobs.
    """
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="crawl-results not implemented yet")


@router.post("/analyse-results")
async def analyse_results(req: AnalyseRequest, apikey: str = Depends(_require_apikey)) -> bool:
    """Accept analysis results. (placeholder)

    TODO: validate payload, persist analysis results, update indices.
    """
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="analyse-results not implemented yet")
