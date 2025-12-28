from typing import List, Optional
from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
	text: Optional[str] = None
	modalities: List[str] = []  # e.g., ["text", "image", "audio", "video"]

class MemoryItem(BaseModel):
	id: Optional[str] = None
	text: str
	metadata: Optional[dict] = None

class SearchQuery(BaseModel):
	query: str
	top_k: int = 5

class AnalyzeResponse(BaseModel):
	reasoning: str
	recommendations: List[str]
	retrieved_context: List[MemoryItem] = []
