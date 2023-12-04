import json
from typing import Any, Iterator

import botocore.eventstream
from ragna.core import Source

from .assistant import BedrockAssistant

# https://huggingface.co/blog/llama2#how-to-prompt-llama-2
INSTRUCTION_TEMPLATE = """
<s>[INST] <<SYS>>
{sources}

{system_prompt}
<</SYS>>

{prompt} [/INST]
""".strip()


class MetaAssistant(BedrockAssistant):
    _PROVIDER = "Meta"

    def _make_request_body(
        self, prompt: str, sources: list[Source], *, max_new_tokens: int
    ) -> dict[str, Any]:
        return {
            "prompt": self._instructize_prompt(prompt, sources),
            "temperature": 0.0,
            "max_gen_len": max_new_tokens,
        }

    def _instructize_prompt(self, prompt: str, sources: list[Source]) -> str:
        return INSTRUCTION_TEMPLATE.format(
            sources="\n\n".join(source.content for source in sources),
            system_prompt=(
                "Use the pieces of context above to answer the prompt. "
                "If you don't know the answer, just say so. "
                "Don't try to make up an answer."
            ),
            prompt=prompt,
        )

    def _parse_response_body(
        self, body: botocore.eventstream.EventStream
    ) -> Iterator[str]:
        for event in body:
            chunk = json.loads(event["chunk"]["bytes"])
            yield chunk["generation"]
            if chunk["stop_reason"] is not None:
                break


class Llama2Chat13B(MetaAssistant):
    _MODEL_ID = "meta.llama2-13b-chat-v1"
    _CONTEXT_SIZE = 4096


class Llama2Chat70B(MetaAssistant):
    _MODEL_ID = "meta.llama2-70b-chat-v1"
    _CONTEXT_SIZE = 4096


class Llama2_13B(MetaAssistant):
    _MODEL_ID = "meta.llama2-13b-v1"
    _CONTEXT_SIZE = 4096


class Llama2_70B(MetaAssistant):
    _MODEL_ID = "meta.llama2-70b-v1"
    _CONTEXT_SIZE = 4096
