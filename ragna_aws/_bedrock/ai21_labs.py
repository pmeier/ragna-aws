import json
from typing import Any, Iterator

import botocore.response
from ragna.core import Source

from .assistant import BedrockAssistant


class Ai21LabsAssistant(BedrockAssistant):
    _PROVIDER = "AI21labs"

    def _make_request_body(
        self, prompt: str, sources: list[Source], *, max_new_tokens: int
    ) -> dict[str, Any]:
        return {
            "prompt": self._instructize_prompt(prompt, sources),
            "maxTokens": max_new_tokens,
            "temperature": 0.0,
        }

    def _instructize_prompt(self, prompt: str, sources: list[Source]) -> str:
        # https://docs.ai21.com/docs/prompt-engineering
        instruction = "\n\n".join(source.content for source in sources)
        instruction += (
            f"##"
            f"Use the pieces of context above to answer the following prompt. "
            f"If you don't know the answer, just say so. "
            f"Don't try to make up an answer.\n\n"
            f"Prompt: {prompt}"
        )
        return instruction

    def _parse_response_body(
        self,
        body: botocore.response.StreamingBody,  # type: ignore[override]
    ) -> Iterator[str]:
        yield json.loads(body.read().decode())["completions"][0]["data"]["text"]


class Jurassic2Ultra(Ai21LabsAssistant):
    _MODEL_ID = "ai21.j2-ultra-v1"
    _CONTEXT_SIZE = 8191


class Jurassic2Mid(Ai21LabsAssistant):
    _MODEL_ID = "ai21.j2-mid-v1"
    _CONTEXT_SIZE = 8191
