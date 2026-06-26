import asyncio
import os
from dotenv import load_dotenv

from adapters.factory import get_ai_adapter
from adapters.base import LLMRequest, LLMMessage

async def main():
    # Load environment variables
    load_dotenv()
    
    print(f"Current AI Provider: {os.getenv('AI_PROVIDER', 'openrouter').upper()}")
    
    try:
        adapter = get_ai_adapter()
    except Exception as e:
        print(f"Failed to initialize adapter: {e}")
        return

    # Simulate a conversation for KPI generation
    messages = [
        LLMMessage(role="system", content="You are a conversation analyst. Based on the user's transcript, extract 3 key KPIs (Key Performance Indicators). Format them clearly."),
        LLMMessage(role="user", content="Transcript: \nAgent: Hello, thanks for calling support. How can I help?\nCustomer: Hi, I've been waiting for 20 minutes. My app keeps crashing on the login screen.\nAgent: I apologize for the wait. Let's get that fixed. Can you tell me your OS version?\nCustomer: iOS 17.\nAgent: Thank you. I see a known issue. I'll send an update to your phone now.")
    ]
    
    request = LLMRequest(messages=messages, temperature=0.5)
    
    print("\n--- Sending request to LLM ---")
    print(f"Model used: {getattr(adapter, '_default_model', 'unknown')}")
    
    try:
        response = await adapter.complete(request)
        print("\n--- Response ---")
        print(response.content)
        print("\n--- Usage Stats ---")
        print(f"Model: {response.model}")
        print(f"Input Tokens: {response.input_tokens}")
        print(f"Output Tokens: {response.output_tokens}")
    except Exception as e:
        print(f"\nError during completion: {e}")

if __name__ == "__main__":
    asyncio.run(main())
