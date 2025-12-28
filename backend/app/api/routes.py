from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional, List
from ..models.schemas import AnalyzeResponse, MemoryItem, SearchQuery
from ..services.asr import ASRService
from ..services.vision import VisionService
from ..services.llm import LLMService
from ..services.embeddings import EmbeddingsService
from ..memory.faiss_store import VectorMemory
from ..utils.media import save_upload

router = APIRouter()

asr_service = ASRService()
vision_service = VisionService()
llm_service = LLMService()
emb_service = EmbeddingsService()
vector_memory = VectorMemory(emb_service)

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
	text: Optional[str] = Form(default=None),
	image: Optional[UploadFile] = File(default=None),
	audio: Optional[UploadFile] = File(default=None),
	video: Optional[UploadFile] = File(default=None),
):
	observations: List[str] = []
	media_paths = {}
	if image is not None:
		media_paths["image"] = await save_upload(image)
		labels = vision_service.describe_image(media_paths["image"])
		observations.append(f"Image: {labels}")
	if audio is not None:
		media_paths["audio"] = await save_upload(audio)
		transcript = asr_service.transcribe(media_paths["audio"])
		observations.append(f"Audio transcript: {transcript}")
	if video is not None:
		media_paths["video"] = await save_upload(video)
		# For simplicity, sample a frame or return mock
		video_summary = vision_service.describe_video(media_paths["video"])
		observations.append(f"Video: {video_summary}")
	if text:
		observations.append(f"User text: {text}")

	retrieved: List[MemoryItem] = []
	if text:
		retrieved = vector_memory.search(text, top_k=5)

	reasoning, recommendations = llm_service.reason(observations, retrieved)

	return AnalyzeResponse(
		reasoning=reasoning,
		recommendations=recommendations,
		retrieved_context=retrieved,
	)

@router.post("/memory/add", response_model=MemoryItem)
async def memory_add(item: MemoryItem) -> MemoryItem:
	stored = vector_memory.add(item.text, metadata=item.metadata)
	return stored

@router.post("/memory/search", response_model=List[MemoryItem])
async def memory_search(query: SearchQuery) -> List[MemoryItem]:
	return vector_memory.search(query.query, top_k=query.top_k)
