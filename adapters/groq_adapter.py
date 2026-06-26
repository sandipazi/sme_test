import os
from openai import AsyncOpenAI
from adapters.base import AbstractAIAdapter, LLMRequest, LLMResponse

class GroqAdapter(AbstractAIAdapter):
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set.")
        self._client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
        )
        self._default_model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    async def complete(self, request: LLMRequest) -> LLMResponse:
        response = await self._client.chat.completions.create(
            model=request.model or self._default_model,
            messages=[{"role": m.role, "content": m.content} for m in request.messages],
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )
        choice = response.choices[0]
        return LLMResponse(
            content=choice.message.content or "",
            model=response.model,
            input_tokens=response.usage.prompt_tokens if response.usage else 0,
            output_tokens=response.usage.completion_tokens if response.usage else 0,
            finish_reason=choice.finish_reason or "stop",
        )
