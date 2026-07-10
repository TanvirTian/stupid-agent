import time
from llm import build_default_client
from memory import ConversationHistory

def main() -> None:
	client =  build_default_client()
	history = ConversationHistory()

	print("basic agent: Phase 1")
	print("Local model: Qwen via ollama")
	print("Type exit or quit to stop.\n")


	while True:
		user_msg = input("you: ").strip()

		if user_msg.lower() in {"exit", "quit"}:
			print("Goodbye!")
			break

		if user_msg.lower() == "clear":
			history.clear()
			print("Conversation history cleared\n")
			continue


		if not user_msg:
			print("please enter a message \n")
			continue

		messages = history.messages_for_next_turn(user_msg)			

		start_time = time.perf_counter()	

		try:
			assistant_reply = client.chat(messages)
		except RuntimeError as exc:
			print(f"Error: {exc}\n")
			continue

		history.add_user_message(user_msg)
		history.add_assistant_message(assistant_reply)	

		end_time = time.perf_counter()

		response_time = end_time - start_time
        

		print(f"Assitant: {assistant_reply}\n")
		print(f"Response time: {response_time:.4f} seconds")


if __name__ == '__main__':
	main()