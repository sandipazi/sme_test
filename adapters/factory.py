import os
from adapters.base import AbstractAIAdapter

def get_ai_adapter() -> AbstractAIAdapter:
    provider = os.getenv("AI_PROVIDER", "openrouter").lower()
    
    if provider == "groq":
        from adapters.groq_adapter import GroqAdapter
        return GroqAdapter()
    elif provider == "openrouter":
        from adapters.openrouter_adapter import OpenRouterAdapter
        return OpenRouterAdapter()
    elif provider == "github":
        from adapters.github_adapter import GitHubAdapter
        return GitHubAdapter()
    elif provider == "gemini":
        from adapters.gemini_adapter import GeminiAdapter
        return GeminiAdapter()
    
    raise ValueError(f"Unknown AI_PROVIDER={provider}. Options: groq, openrouter, github, gemini")
