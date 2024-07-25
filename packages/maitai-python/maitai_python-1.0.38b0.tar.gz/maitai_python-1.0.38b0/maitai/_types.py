from datetime import datetime
from typing import Mapping, Union

import openai.types.chat as openai_chat_types
from betterproto import Casing
from typing_extensions import Literal

from maitai_gen.chat import ChatCompletionChunk, ChatCompletionResponse, EvaluateRequest, EvaluateResponse


class Omit:
    def __bool__(self) -> Literal[False]:
        return False


Headers = Mapping[str, Union[str, Omit]]
Query = Mapping[str, object]
Body = object


class MaitaiChunk(ChatCompletionChunk):
    def __init__(self, chat_completion_chunk: ChatCompletionChunk = None):
        super().__init__()
        if chat_completion_chunk is not None:
            if chat_completion_chunk.evaluate_response is not None:
                self.evaluate_response = EvaluateResponse(evaluation_request=EvaluateRequest())
            self.from_pydict(chat_completion_chunk.to_pydict())

    def model_dump_json(self):
        return self.to_pydict(casing=Casing.SNAKE)

    def openai_dump_json(self):
        data = self.to_pydict(casing=Casing.SNAKE)
        if not data.get("choices"):
            data["choices"] = []
        if not data.get("created"):
            data["created"] = int(datetime.utcnow().timestamp())
        for i, choice in enumerate(data.get("choices")):
            if choice.get("finish_reason") == "end_turn":
                choice["finish_reason"] = "stop"
            if not choice.get("index"):
                choice["index"] = i
            if not choice.get("delta"):
                choice["delta"] = {
                }
            if choice["delta"].get("tool_calls"):
                for j, tool_call in enumerate(choice["delta"]["tool_calls"]):
                    if not tool_call.get("index"):
                        tool_call["index"] = j
        if data.get("usage"):
            if not data["usage"].get("prompt_tokens"):
                data["usage"]["prompt_tokens"] = 0
            if not data["usage"].get("completion_tokens"):
                data["usage"]["completion_tokens"] = 0
        return openai_chat_types.ChatCompletionChunk(**data).model_dump_json()


class MaitaiCompletion(ChatCompletionResponse):
    def __init__(self, chat_completion_response: ChatCompletionResponse = None):
        super().__init__()
        if chat_completion_response is not None:
            if chat_completion_response.evaluate_response is not None:
                self.evaluate_response = EvaluateResponse(evaluation_request=EvaluateRequest())
            self.from_pydict(chat_completion_response.to_pydict())

    def model_dump_json(self):
        return self.to_pydict(casing=Casing.SNAKE)

    def openai_dump_json(self):
        data = self.to_pydict(casing=Casing.SNAKE)
        for i, choice in enumerate(data.get("choices")):
            if not choice.get("index"):
                choice["index"] = i
            if choice.get("finish_reason") == "end_turn":
                choice["finish_reason"] = "stop"
            if choice.get("message", {}).get("tool_calls"):
                for j, tool_call in enumerate(choice["message"]["tool_calls"]):
                    if not tool_call.get("index"):
                        tool_call["index"] = j
        return openai_chat_types.ChatCompletion(**data).model_dump_json()
