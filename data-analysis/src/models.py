from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional

class AnalyzeRequest(BaseModel):
    content: str = Field(..., description="Content to be analyzed")
    callbackUrl: Optional[HttpUrl] = Field(
        None,
        description="Optional override URL to POST analysis result to"
    )

class JobAccepted(BaseModel):
    jobId: str

class AnalysisResult(BaseModel):
    tags: List[str]
    title: Optional[str] = None
    legality: bool
    description: Optional[str] = None
    url: Optional[str] = None
    jobId: str
