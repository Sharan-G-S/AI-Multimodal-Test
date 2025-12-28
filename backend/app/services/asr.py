from typing import Optional
from ..core.config import settings

class ASRService:
	def __init__(self) -> None:
		self.use_mock = settings.use_mock_models
		# Real whisper initialization would go here

	def transcribe(self, audio_path: str) -> str:
		if self.use_mock:
			return "[mock] transcribed audio content"
		# Implement whisper transcription if enabled
		raised_msg = (
			"ASR (Whisper) not enabled. Set use_mock_models=False and install dependencies."
		)
		raise RuntimeError(raised_msg)
