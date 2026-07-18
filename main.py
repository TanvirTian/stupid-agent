from agent import BasicAgent
from llm import build_default_client
from memory import ConversationHistory


def main() -> None:
    client = build_default_client()
    history = ConversationHistory()
    agent = BasicAgent(client=client, history=history)

    print("Stupid-Agent")
    print("Local model: Qwen via Ollama")
    print("Try asking: Read notes.txt and summarize it.")
    print("Type 'clear' to reset conversation history.")
    print("Type 'exit' or 'quit' to stop.\n")
    
    while True:
        user_message = input("You: ").strip()

        if user_message.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if user_message.lower() == "clear":
            history.clear()
            print("Conversation history cleared.\n")
            continue

        if not user_message:
            print("Please enter a message.\n")
            continue

        try:
            assistant_reply = agent.run(user_message)
        except RuntimeError as exc:
            print(f"Error: {exc}\n")
            continue

        print(f"Assistant: {assistant_reply}\n")


if __name__ == "__main__":
    main()

