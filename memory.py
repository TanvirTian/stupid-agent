from dataclasses import dataclass

@dataclass(frozen=True)
class ChatMessage:
	role: str
	content: str


class ConversationHistory:
	def __init__(self) -> None:
		self._messages: list[ChatMessage] = [] 

	def add_user_message(self, content: str) -> None:
		self._messages.append(ChatMessage(role="user", content=content))

	def add_assistant_message(self, content: str) -> None:
		self._messages.append(ChatMessage(role="assistant", content=content))


	def to_ollama_message(self) -> list[dict[str, str]]:
		return [
			{"role": message.role, "content": message.content}
			for message in self._messages

		]

	
	def messages_for_next_turn(self, user_msg: str) -> list[dict[str, str]]:
		messages = self.to_ollama_message()
		messages.append({"role": "user", "content": user_msg})
		return messages

	def clear(self) -> None:
		self._messages.clear()	