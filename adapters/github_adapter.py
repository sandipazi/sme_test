import os
from openai import AsyncOpenAI
from adapters.base import AbstractAIAdapter, LLMRequest, LLMResponse

class GitHubAdapter(AbstractAIAdapter):
    def __init__(self):
        api_key = os.getenv("GITHUB_TOKEN")
        if not api_key:
            raise ValueError("GITHUB_TOKEN is not set.")
        self._client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://models.inference.ai.azure.com",
        )
        self._default_model = os.getenv("GITHUB_MODEL", "gpt-4o-mini")

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
