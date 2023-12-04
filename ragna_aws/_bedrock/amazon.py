import json
from typing import Any, Iterator

import botocore.eventstream
from ragna.core import Source

from .assistant import BedrockAssistant


class AmazonAssistant(BedrockAssistant):
    _PROVIDER = "Amazon"

    def _make_request_body(
        self, prompt: str, sources: list[Source], *, max_new_tokens: int
    ) -> dict[str, Any]:
        return {
            "inputText": self._instructize_prompt(prompt, sources),
            "textGenerationConfig": {
                "temperature": 0.0,
                "maxTokenCount": max_new_tokens,
                "stopSequences": ["User:"],
            },
        }

    def _instructize_prompt(self, prompt: str, sources: list[Source]) -> str:
        # See https://d2eo22ngex1n9g.cloudfront.net/Documentation/User+Guides/Titan/Amazon+Titan+Text+Prompt+Engineering+Guidelines.pdf
        instruction = (
            "Use the following pieces of context to answer the question at the end. "
            "If you don't know the answer, just say so. Don't try to make up an answer.\n"
        )
        instruction += "\n\n".join(source.content for source in sources)
        return f"{instruction}\n\nUser: {prompt}\n\nBot:"

    def _parse_response_body(
        self, body: botocore.eventstream.EventStream
    ) -> Iterator[str]:
        for event in body:
            yield json.loads(event.get("chunk")["bytes"])["outputText"]


class TitanTextExpress(AmazonAssistant):
    # https://docs.aws.amazon.com/bedrock/latest/userguide/titan-text-models.html
    _MODEL_ID = "amazon.titan-text-express-v1"
    _CONTEXT_SIZE = 8_000


class TitanTextLite(AmazonAssistant):
    # https://docs.aws.amazon.com/bedrock/latest/userguide/titan-text-models.html
    _MODEL_ID = "amazon.titan-text-lite-v1"
    _CONTEXT_SIZE = 4_000
