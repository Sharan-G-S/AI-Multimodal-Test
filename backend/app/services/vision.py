from ..core.config import settings

class VisionService:
	def __init__(self) -> None:
		self.use_mock = settings.use_mock_models

	def describe_image(self, image_path: str) -> str:
		if self.use_mock:
			return "[mock] objects: bolt, wrench, metal panel"
		raise RuntimeError("Vision model not enabled. Set use_mock_models=False and implement model.")

	def describe_video(self, video_path: str) -> str:
		if self.use_mock:
			return "[mock] video summary: rotating tool near loose bolt"
		raise RuntimeError("Video model not enabled. Set use_mock_models=False and implement model.")
