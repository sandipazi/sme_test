import os
from openai import AsyncOpenAI
from adapters.base import AbstractAIAdapter, LLMRequest, LLMResponse

class GeminiAdapter(AbstractAIAdapter):
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        self._client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
        self._default_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

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
