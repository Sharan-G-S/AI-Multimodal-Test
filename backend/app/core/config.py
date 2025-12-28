from pydantic import Field
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
	model_config = {
		"env_file": ".env",
		"protected_namespaces": ("settings_",),
	}

	cors_allow_origins: List[str] = Field(default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173"]) 
	model_device: str = Field(default="cpu")
	use_mock_models: bool = Field(default=True)
	embedding_model_name: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")

settings = Settings()
