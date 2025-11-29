from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class SearchRequest(BaseModel):
    query: str

class SearchResponse(BaseModel):
    results: list[str]

@router.post("/search", response_model=SearchResponse)
async def search_data(request: SearchRequest):
    query = request.query.strip()
    
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    # Simuliere Such-Ergebnisse
    # Hier würde der Aufruf an deinen nächsten Service gehen
    dummy_results = [
        f"Result 1 for: {query}",
        f"Result 2 for: {query}",
        f"Result 3 for: {query}"
    ]
    
    return SearchResponse(results=dummy_results)