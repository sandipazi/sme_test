from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class LLMMessage:
    role: str
    content: str

@dataclass
class LLMRequest:
    messages: list[LLMMessage]
    model: str | None = None
    max_tokens: int = 4096
    temperature: float = 0.7

@dataclass
class LLMResponse:
    content: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    finish_reason: str = "stop"

class AbstractAIAdapter(ABC):
    @abstractmethod
    async def complete(self, request: LLMRequest) -> LLMResponse:
        ...
