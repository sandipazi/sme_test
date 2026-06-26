import asyncio
import os
import json
import sqlite3
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

from adapters.factory import get_ai_adapter
from adapters.base import LLMRequest, LLMMessage

def get_transcripts_from_json(filepath="data.json"):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        data = json.load(f)
        if isinstance(data, list):
            return [item.get("transcript", "") for item in data]
        return [data.get("transcript", "")]

def get_transcripts_from_db(db_path="test.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transcript TEXT
        )
    """)
    cursor.execute("SELECT transcript FROM conversations ORDER BY id ASC")
    rows = cursor.fetchall()
    if not rows:
        sample_texts = [
            "Agent: Hello from SQLite support.\nCustomer: Hi, my queries are running very slow.\nAgent: Let's check your indexes. Have you run an EXPLAIN QUERY PLAN?\nCustomer: Not yet, I will do that now.",
            "Agent: Support here.\nCustomer: My database is locked.\nAgent: That usually means a transaction was left open. Let's kill the idle connections."
        ]
        for text in sample_texts:
            cursor.execute("INSERT INTO conversations (transcript) VALUES (?)", (text,))
        conn.commit()
        transcripts = sample_texts
    else:
        transcripts = [row[0] for row in rows]
    conn.close()
    return transcripts

async def main():
    # Load environment variables
    load_dotenv()
    
    print(f"Current AI Provider: {os.getenv('AI_PROVIDER', 'openrouter').upper()}")
    
    try:
        adapter = get_ai_adapter()
    except Exception as e:
        print(f"Failed to initialize adapter: {e}")
        return

    # Determine data source
    data_source = os.getenv("DATA_SOURCE", "manual").lower()
    
    if data_source == "json":
        print("Loading transcripts from JSON (data.json)...")
        transcripts = get_transcripts_from_json()
    elif data_source == "database":
        print("Loading transcripts from Database (test.db)...")
        transcripts = get_transcripts_from_db()
    else:
        print("Using manual transcripts...")
        transcripts = [
            "Agent: Hello, thanks for calling support. How can I help?\nCustomer: Hi, I've been waiting for 20 minutes. My app keeps crashing on the login screen.\nAgent: I apologize for the wait. Let's get that fixed. Can you tell me your OS version?\nCustomer: iOS 17.\nAgent: Thank you. I see a known issue. I'll send an update to your phone now.",
            "Agent: Product support, John speaking.\nCustomer: How do I reset my password?\nAgent: You can click the 'Forgot Password' link on the login screen."
        ]

    print(f"\nFound {len(transcripts)} conversations to process.")

    # Process each conversation
    for i, transcript in enumerate(transcripts, start=1):
        print(f"\n{'='*50}")
        print(f"Processing Conversation {i}/{len(transcripts)}")
        print(f"{'='*50}")
        
        messages = [
            LLMMessage(role="system", content="You are a conversation analyst. Based on the user's transcript, extract 3 key KPIs (Key Performance Indicators). Format them clearly."),
            LLMMessage(role="user", content=f"Transcript: \n{transcript}")
        ]
        
        request = LLMRequest(messages=messages, temperature=0.5)
        
        print(f"Model used: {getattr(adapter, '_default_model', 'unknown')}")
        
        try:
            response = await adapter.complete(request)
            print("\n--- Extracted KPIs ---")
            print(response.content)
            print("\n--- Usage Stats ---")
            print(f"Model: {response.model}")
            print(f"Input Tokens: {response.input_tokens}")
            print(f"Output Tokens: {response.output_tokens}")
        except Exception as e:
            print(f"\nError during completion: {e}")

if __name__ == "__main__":
    asyncio.run(main())
