from pydantic import BaseModel, Field
from typing import List, Optional

class Content(BaseModel):
    content: str = Field(..., description="Content of site to be analyzed")
