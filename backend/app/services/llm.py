from typing import List, Tuple
from ..core.config import settings
from ..models.schemas import MemoryItem

class LLMService:
	def __init__(self) -> None:
		self.use_mock = settings.use_mock_models

	def reason(self, observations: List[str], retrieved: List[MemoryItem]) -> Tuple[str, List[str]]:
		if self.use_mock:
			reasoning = (
				"Based on observations, the part appears to involve fasteners; the next step is to use an appropriate tool."
			)
			recs = [
				"Use a socket wrench sized to the bolt head",
				"Stabilize the panel to avoid slippage",
			]
			if any("loose" in obs.lower() for obs in observations):
				recs.append("Tighten to manufacturer torque spec")
			if len(retrieved) > 0:
				reasoning += " Retrieved relevant past notes to guide the decision."
			return reasoning, recs
		raise RuntimeError("LLM not configured. Set use_mock_models=False and integrate a provider.")
