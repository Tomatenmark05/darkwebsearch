from fastapi import FastAPI
from routers import crawler

app = FastAPI(
    title="Darkwebsearch - Crawler API",
    version="1.0.0",
    description="API for starting dark web crawls and retrieving crawl status.",
)

app.include_router(crawler.router, tags=["Crawl"])

