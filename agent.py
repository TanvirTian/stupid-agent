from dataclasses import dataclass

from llm import OllamaClient
from memory import ConversationHistory
from prompts import SYSTEM_PROMPT
from tools import ToolError, run_tool


@dataclass(frozen=True)
class ToolRequest:
    tool_name: str
    tool_input: str


class StupidAgent:
    def __init__(self, client: OllamaClient, history: ConversationHistory) -> None:
        self.client = client
        self.history = history

    def run(self, user_message: str) -> str:
        initial_messages = self._build_messages_for_user_turn(user_message)
        first_reply = self.client.chat(initial_messages)

        tool_request = self._parse_tool_request(first_reply)

        if tool_request is None:
            self._commit_turn(user_message, first_reply)
            return first_reply

        print(f"[tool] {tool_request.tool_name}({tool_request.tool_input})")

        tool_output = self._execute_tool(tool_request)

        final_messages = self._build_messages_with_tool_result(
            initial_messages=initial_messages,
            assistant_tool_request=first_reply,
            tool_request=tool_request,
            tool_output=tool_output,
        )

        final_reply = self.client.chat(final_messages)

        self._commit_turn(user_message, final_reply)
        return final_reply

    def _build_messages_for_user_turn(self, user_message: str) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": SYSTEM_PROMPT},
            *self.history.messages_for_next_turn(user_message),
        ]

    def _parse_tool_request(self, model_reply: str) -> ToolRequest | None:
        lines = [line.strip() for line in model_reply.strip().splitlines() if line.strip()]

        if not lines:
            return None

        if not lines[0].startswith("ACTION:"):
            return None

        if len(lines) != 2:
            raise RuntimeError(f"Invalid tool request format: {model_reply}")

        tool_name = lines[0][len("ACTION:"):].strip()

        if not lines[1].startswith("ACTION_INPUT:"):
            raise RuntimeError(f"Invalid tool request format: {model_reply}")

        tool_input = lines[1][len("ACTION_INPUT:"):].strip()

        if not tool_name:
            raise RuntimeError("Tool request is missing a tool name.")

        if not tool_input:
            raise RuntimeError("Tool request is missing tool input.")

        return ToolRequest(tool_name=tool_name, tool_input=tool_input)

    def _execute_tool(self, tool_request: ToolRequest) -> str:
        try:
            return run_tool(tool_request.tool_name, tool_request.tool_input)
        except ToolError as exc:
            return f"TOOL ERROR: {exc}"

    def _build_messages_with_tool_result(
        self,
        initial_messages: list[dict[str, str]],
        assistant_tool_request: str,
        tool_request: ToolRequest,
        tool_output: str,
    ) -> list[dict[str, str]]:
        tool_result_message = (
            "TOOL RESULT:\n"
            f"TOOL_NAME: {tool_request.tool_name}\n"
            f"TOOL_INPUT: {tool_request.tool_input}\n"
            f"TOOL_OUTPUT:\n{tool_output}\n\n"
            "Use this result to answer the user's original request."
        )

        return [
            *initial_messages,
            {"role": "assistant", "content": assistant_tool_request},
            {"role": "user", "content": tool_result_message},
        ]

    def _commit_turn(self, user_message: str, assistant_reply: str) -> None:
        self.history.add_user_message(user_message)
        self.history.add_assistant_message(assistant_reply)