from pathlib import Path  
from config import settings

class ToolError(Exception):
	pass


def get_files_directory() -> Path:
	    return (Path(__file__).resolve().parent / 
settings.files_directory_name).resolve()		


def resolve_file_path(user_path: str) -> Path:
	cleaned_path = user_path.strip()

	if not cleaned_path:
		raise ToolError("usage: /read <relative-file-path>")

	candidate_path = Path(cleaned_path)

	if candidate_path.is_absolute():
		raise ToolError("Please use a relative path inside the files directory")

	files_directory = get_files_directory()
	target_path = (files_directory / candidate_path).resolve()

	try:
		target_path.relative_to(files_directory)
	except ValueError as exc:
		raise ToolError("That path escaeps the allowed files directory") from exc 
	
	return target_path

	
def read_text_file(user_path: str) -> str:
	target_path = resolve_file_path(user_path)

	if not target_path.exists():
		raise ToolError(f"File not found: {target_path.name}")

	if not target_path.is_file():
		raise ToolError(f"Not a file: {target_path.name}")

	try:
		content = target_path.read_text(encoding="utf-8")
	except UnicodeDecodeError as exc:
		raise ToolError("Only UTF-8 text files are supported.") from exc 

	if len(content) > settings.max_file_characters:
		truncated_content = content[:settings.max_file_characters]
		return (
			f"{truncated_content}\n\n"
			f"[File truncated to first {settings.max_file_characters} characters.]"
			)	

	return content 					


def run_tool(tool_name: str, tool_input: str) -> str:
	if tool_name == "read_text_file":
		return read_text_file(tool_input)
	raise ToolError(f"Unknown tool: {tool_name}")	