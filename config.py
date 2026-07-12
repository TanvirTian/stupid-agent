from dataclasses import dataclass  

@dataclass(frozen=True)
class Settings:
	ollama_base_url: str = "http://localhost:11434"
	model_name: str = "qwen2.5:7b"
	timeout: int = 120 
	files_directory_name: str = "files"
	max_file_characters: int = 5000 


settings = Settings()