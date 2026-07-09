from dataclasses import dataclass  

@dataclass(frozen=True)
class Settings:
	ollama_base_url: str = "http://localhost:11434"
	model_name: str = "qwen2.5:7b"
	timeout: int = 120  


settings = Settings()