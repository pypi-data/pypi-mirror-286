from typing import Mapping, Union

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


class MaitaiCompletion(ChatCompletionResponse):
    def __init__(self, chat_completion_response: ChatCompletionResponse = None):
        super().__init__()
        if chat_completion_response is not None:
            if chat_completion_response.evaluate_response is not None:
                self.evaluate_response = EvaluateResponse(evaluation_request=EvaluateRequest())
            self.from_pydict(chat_completion_response.to_pydict())

    def model_dump_json(self):
        return self.to_pydict(casing=Casing.SNAKE)
