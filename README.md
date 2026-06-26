# SME Modal Test - Multi-LLM Adapter Sandbox

This repository provides a sandbox environment to test various Large Language Models (LLMs) for your Conversation Analyst backend without making structural changes to your core application. 

It implements an **Adapter Pattern** exactly as it would function in your main FastAPI backend, allowing you to seamlessly swap out the underlying LLM simply by updating an environment variable.

## Supported Providers

This project is configured to use third-party aggregator APIs that offer extremely generous free tiers or demo access to high-tier models.

1. **OpenRouter**: Excellent for testing a wide variety of open-source and proprietary models (many for free).
2. **Groq**: Excellent for ultra-fast inference on Llama and Qwen models.
3. **GitHub Models**: Great for free access to GPT-4o mini and Phi-3 models (requires GitHub Models beta).
4. **Gemini**: Directly accesses Google's generative AI endpoint via OpenAI compatibility.

## Setup Instructions

### 1. Install Dependencies
Ensure you have Python installed, then install the required libraries:
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy the example environment file:
```bash
cp .env.example .env
```
Open `.env` and add your API keys. You can generate free API keys at:
- OpenRouter: [https://openrouter.ai/keys](https://openrouter.ai/keys)
- Groq: [https://console.groq.com/keys](https://console.groq.com/keys)
- GitHub Models: [https://github.com/settings/tokens](https://github.com/settings/tokens)
- Gemini API: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### 3. Choose your Data Source
In `.env`, you can set `DATA_SOURCE` to determine where the transcript comes from:
- `manual` (default): Uses a hardcoded string in `main.py`.
- `json`: Loads from `data.json`.
- `database`: Loads from a local SQLite database (`test.db`). If none exists, it will automatically create and populate one with a sample transcript!

## Testing Models

To test a specific model, modify your `.env` file to set the `AI_PROVIDER` and the corresponding model variable, then run the script.

### Using OpenRouter
Set the following in `.env`:
```env
AI_PROVIDER=openrouter
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free
```

**Free Models available on OpenRouter to test:**
- Meta Llama 3.1 8B: `meta-llama/llama-3.1-8b-instruct:free`
- Alibaba Qwen 2.5 7B: `qwen/qwen-2.5-7b-instruct:free`
- Microsoft Phi-3 Small: `microsoft/phi-3-mini-128k-instruct:free`
- DeepSeek R1 Distill: `deepseek/deepseek-r1-distill-qwen-7b:free`
- Google Gemini 2.0 Flash: `google/gemini-2.0-flash:free`

### Using Groq
Set the following in `.env`:
```env
AI_PROVIDER=groq
GROQ_MODEL=llama-3.1-8b-instant
```

### Using GitHub Models
Set the following in `.env`:
```env
AI_PROVIDER=github
GITHUB_TOKEN=ghp_...
GITHUB_MODEL=gpt-4o-mini
```

### Using Gemini Models
Set the following in `.env`:
```env
AI_PROVIDER=gemini
GEMINI_API_KEY=AIza...
GEMINI_MODEL=gemini-2.0-flash
```

## Running the Test

Once your `.env` is configured, run the main testing script:
```bash
python main.py
```

The script will:
1. Initialize the correct Adapter (Groq or OpenRouter).
2. Feed a simulated customer support transcript to the AI.
3. Ask the AI to extract 3 KPIs.
4. Print the AI's response along with token usage statistics.
