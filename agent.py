import json
from dataclasses import dataclass
from json import JSONDecodeError

from llm import OllamaClient
from memory import ConversationHistory
from prompts import SYSTEM_PROMPT
from tools import ToolError, run_tool


@dataclass(frozen=True)
class ToolRequest:
    tool_name: str
    tool_input: str


@dataclass(frozen=True)
class FinalAnswer:
    content: str


class BasicAgent:
    def __init__(self, client: OllamaClient, history: ConversationHistory) -> None:
        self.client = client
        self.history = history

    def run(self, user_message: str) -> str:
        initial_messages = self._build_messages_for_user_turn(user_message)
        first_reply_text = self.client.chat(initial_messages)
        first_decision = self._parse_model_reply(first_reply_text)

        if isinstance(first_decision, FinalAnswer):
            self._commit_turn(user_message, first_decision.content)
            return first_decision.content

        print(f"[tool] {first_decision.tool_name}({first_decision.tool_input})")

        tool_output = self._execute_tool(first_decision)

        final_messages = self._build_messages_with_tool_result(
            initial_messages=initial_messages,
            assistant_tool_request=first_reply_text,
            tool_request=first_decision,
            tool_output=tool_output,
        )

        second_reply_text = self.client.chat(final_messages)
        second_decision = self._parse_model_reply(second_reply_text)

        if not isinstance(second_decision, FinalAnswer):
            raise RuntimeError(
                "Expected a final JSON answer after tool result, "
                "but the model requested another tool."
            )

        self._commit_turn(user_message, second_decision.content)
        return second_decision.content

    def _build_messages_for_user_turn(self, user_message: str) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": SYSTEM_PROMPT},
            *self.history.messages_for_next_turn(user_message),
        ]

    def _strip_code_fences(self, model_reply: str) -> str:
        cleaned_reply = model_reply.strip()

        if not cleaned_reply.startswith("```"):
            return cleaned_reply

        lines = cleaned_reply.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        return "\n".join(lines).strip()

    def _parse_model_reply(self, model_reply: str) -> FinalAnswer | ToolRequest:
        cleaned_reply = self._strip_code_fences(model_reply)

        try:
            data = json.loads(cleaned_reply)
        except JSONDecodeError as exc:
            raise RuntimeError(f"Model did not return valid JSON: {model_reply}") from exc

        if not isinstance(data, dict):
            raise RuntimeError("Model response must be a JSON object.")

        response_type = data.get("type")

        if response_type == "final":
            content = data.get("content")

            if not isinstance(content, str) or not content.strip():
                raise RuntimeError(
                    "Final response must include a non-empty string field 'content'."
                )

            return FinalAnswer(content=content.strip())

        if response_type == "tool_call":
            tool_name = data.get("tool_name")
            tool_input = data.get("tool_input")

            if not isinstance(tool_name, str) or not tool_name.strip():
                raise RuntimeError(
                    "Tool call must include a non-empty string field 'tool_name'."
                )

            if not isinstance(tool_input, str) or not tool_input.strip():
                raise RuntimeError(
                    "Tool call must include a non-empty string field 'tool_input'."
                )

            return ToolRequest(
                tool_name=tool_name.strip(),
                tool_input=tool_input.strip(),
            )

        raise RuntimeError(f"Unknown response type: {response_type}")

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
            "Return a final JSON answer using this result."
        )

        return [
            *initial_messages,
            {"role": "assistant", "content": assistant_tool_request},
            {"role": "user", "content": tool_result_message},
        ]

    def _commit_turn(self, user_message: str, assistant_reply: str) -> None:
        self.history.add_user_message(user_message)
        self.history.add_assistant_message(assistant_reply)