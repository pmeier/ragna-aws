import json
from typing import Any, Iterator

import botocore.eventstream
from ragna.core import Source

from .assistant import BedrockAssistant


class AnthropicAssistant(BedrockAssistant):
    _PROVIDER = "Anthropic"

    def _make_request_body(
        self, prompt: str, sources: list[Source], *, max_new_tokens: int
    ) -> dict[str, Any]:
        return {
            "prompt": self._instructize_prompt(prompt, sources),
            "temperature": 0.0,
            "max_tokens_to_sample": max_new_tokens,
        }

    def _instructize_prompt(self, prompt: str, sources: list[Source]) -> str:
        # See https://docs.anthropic.com/claude/docs/introduction-to-prompt-design#human--assistant-formatting
        instruction = (
            "\n\nHuman: "
            "Use the following pieces of context to answer the question at the end. "
            "If you don't know the answer, just say so. Don't try to make up an answer.\n"
        )
        instruction += "\n\n".join(source.content for source in sources)
        return f"{instruction}\n\nQuestion: {prompt}\n\nAssistant:"

    def _parse_response_body(
        self, body: botocore.eventstream.EventStream
    ) -> Iterator[str]:
        for event in body:
            chunk = json.loads(event["chunk"]["bytes"])
            yield chunk["completion"]


class Claude(AnthropicAssistant):
    _MODEL_ID = "anthropic.claude-v2:1"
    _CONTEXT_SIZE = 100_000


class ClaudeInstant(AnthropicAssistant):
    _MODEL_ID = "anthropic.claude-instant-v1"
    _CONTEXT_SIZE = 100_000
