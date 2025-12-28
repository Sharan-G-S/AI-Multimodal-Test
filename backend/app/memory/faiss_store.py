from __future__ import annotations
from typing import List, Optional
import uuid
import faiss
import numpy as np
from ..models.schemas import MemoryItem

class VectorMemory:
	def __init__(self, embeddings_service) -> None:
		self.emb = embeddings_service
		self.dim = 384  # aligns with mock or MiniLM default
		self.index = faiss.IndexFlatIP(self.dim)
		self.items: List[MemoryItem] = []
		self.norm = True

	def _normalize(self, vectors: np.ndarray) -> np.ndarray:
		if not self.norm:
			return vectors
		norms = np.linalg.norm(vectors, axis=1, keepdims=True) + 1e-12
		return vectors / norms

	def add(self, text: str, metadata: Optional[dict] = None) -> MemoryItem:
		vec = self.emb.embed([text])
		vec = self._normalize(vec)
		self.index.add(vec)
		item = MemoryItem(id=str(uuid.uuid4()), text=text, metadata=metadata or {})
		self.items.append(item)
		return item

	def search(self, query: str, top_k: int = 5) -> List[MemoryItem]:
		if len(self.items) == 0:
			return []
		q = self.emb.embed([query])
		q = self._normalize(q)
		distances, indices = self.index.search(q, min(top_k, len(self.items)))
		idxs = [i for i in indices[0] if i != -1]
		return [self.items[i] for i in idxs]
