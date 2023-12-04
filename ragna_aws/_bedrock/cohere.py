import json
from typing import Any, Iterator

import botocore.eventstream
from ragna.core import Source

from .assistant import BedrockAssistant


class CohereAssistant(BedrockAssistant):
    _PROVIDER = "Cohere"

    def _make_request_body(
        self, prompt: str, sources: list[Source], *, max_new_tokens: int
    ) -> dict[str, Any]:
        return {
            "prompt": self._instructize_prompt(prompt, sources),
            "temperature": 0.0,
            "max_tokens": max_new_tokens,
            "stream": True,
        }

    def _instructize_prompt(self, prompt: str, sources: list[Source]) -> str:
        instruction = "\n\n".join(source.content for source in sources)
        instruction += (
            f"\n\n"
            f"Use the pieces of context above to answer the following prompt. "
            f"If you don't know the answer, just say so. "
            f"Don't try to make up an answer.\n\n"
            f"Prompt: {prompt}"
        )
        return instruction

    def _parse_response_body(
        self, body: botocore.eventstream.EventStream
    ) -> Iterator[str]:
        for event in body:
            chunk = json.loads(event["chunk"]["bytes"])
            if chunk["is_finished"]:
                break
            yield chunk["text"]


class Command(CohereAssistant):
    # https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids-arns.html
    _MODEL_ID = "cohere.command-text-v14"
    # https://docs.cohere.com/docs/models#command
    _CONTEXT_SIZE = 4096


class CommandLight(CohereAssistant):
    # https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids-arns.html
    _MODEL_ID = "cohere.command-light-text-v14"
    # https://docs.cohere.com/docs/models#command
    _CONTEXT_SIZE = 4096
