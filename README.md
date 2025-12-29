# Cognitive Multimodal AI Agent

> **A multimodal AI agent is an advanced artificial intelligence system that can process, understand, and generate information across multiple data types (modalities) simultaneously, like text, images, audio, and video, giving it a more human-like, holistic perception of the world to perform complex tasks, learn, and act autonomously.**

---

FastAPI backend providing multimodal analysis (text/image/audio/video) and vector memory. Uses mock models by default to run light-weight locally.

## Prerequisites
- Python 3.11+
- macOS (tested), Linux should also work

## Setup
```bash
# From repo root
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt
```

## Run backend
```bash
# From repo root (venv active)
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

Health check:
- GET http://localhost:8000/health

API endpoints:
- POST http://localhost:8000/api/analyze (multipart form: optional text, image, audio, video)
- POST http://localhost:8000/api/memory/add (json: { text, metadata? })
- POST http://localhost:8000/api/memory/search (json: { query, top_k })

## Notes
- Mock mode is on by default (`use_mock_models=True`). To use real models, set `use_mock_models=False` in `backend/app/core/config.py` and install the required libraries (PyTorch, sentence-transformers, Whisper, etc.).
- Uploaded files are stored at `backend/storage`.

---

Made with 💚 from Sharan
