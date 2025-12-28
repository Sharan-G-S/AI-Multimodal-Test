import os
from pathlib import Path
from fastapi import UploadFile

BASE_DIR = Path("/Users/sharan/AI-Multimodal/backend/storage")
BASE_DIR.mkdir(parents=True, exist_ok=True)

aSYNC_CHUNK = 1024 * 1024

async def save_upload(file: UploadFile) -> str:
	path = BASE_DIR / file.filename
	with path.open("wb") as f:
		while True:
			chunk = await file.read(aSYNC_CHUNK)
			if not chunk:
				break
			f.write(chunk)
	return str(path)
