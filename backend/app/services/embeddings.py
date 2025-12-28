from typing import List
import numpy as np
from ..core.config import settings

class EmbeddingsService:
	def __init__(self) -> None:
		self.use_mock = settings.use_mock_models
		self.model_name = settings.embedding_model_name
		self._model = None

	def _ensure_model(self) -> None:
		if self._model is None and not self.use_mock:
			try:
				from sentence_transformers import SentenceTransformer  # type: ignore
			except Exception as exc:  # pragma: no cover
				raise RuntimeError(
					"sentence-transformers is required when use_mock_models=False. Install it and torch."
				) from exc
			self._model = SentenceTransformer(self.model_name, device=settings.model_device)

	def embed(self, texts: List[str]) -> np.ndarray:
		if self.use_mock:
			# Deterministic pseudo-random embeddings for stability in mock mode
			rng = np.random.default_rng(abs(hash("\n".join(texts))) % (2**32))
			return rng.standard_normal((len(texts), 384)).astype("float32")
		self._ensure_model()
		embs = self._model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
		return embs.astype("float32")
