import abc
import json
from typing import Any, Iterator

import boto3
import botocore.eventstream
import botocore.response
from ragna.core import Assistant, Config, Source

# https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters.html
# https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids-arns.html


class BedrockAssistant(Assistant):
    _PROVIDER: str
    _MODEL_ID: str
    _CONTEXT_SIZE: int

    @classmethod
    def display_name(cls) -> str:
        return f"{cls._PROVIDER}/{cls._MODEL_ID}"

    def __init__(self, config: Config) -> None:
        super().__init__(config)

        bedrock = boto3.client("bedrock")
        self._supports_streaming = bedrock.get_foundation_model(
            modelIdentifier=self._MODEL_ID
        )["modelDetails"].get("responseStreamingSupported", False)

        self._brt = boto3.client("bedrock-runtime")

    @property
    def max_input_size(self) -> int:
        return self._CONTEXT_SIZE

    def answer(
        self, prompt: str, sources: list[Source], *, max_new_tokens: int = 256
    ) -> str:
        invoke = getattr(
            self._brt,
            "invoke_model_with_response_stream"
            if self._supports_streaming
            else "invoke_model",
        )
        response = invoke(
            body=json.dumps(
                self._make_request_body(prompt, sources, max_new_tokens=max_new_tokens)
            ),
            modelId=self._MODEL_ID,
            accept="application/json",
            contentType="application/json",
        )
        return "".join(self._parse_response_body(response.get("body")))

    @abc.abstractmethod
    def _make_request_body(
        self, prompt: str, sources: list[Source], *, max_new_tokens: int
    ) -> dict[str, Any]:
        pass

    @abc.abstractmethod
    def _parse_response_body(
        self, body: botocore.eventstream.EventStream
    ) -> Iterator[str]:
        pass
