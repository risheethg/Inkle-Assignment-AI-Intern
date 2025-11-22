# Quick Start Guide - Backend

## WARNING: Before Running the Server

You need to set up your `.env` file with API keys!

### Step 1: Create .env file

Copy the example file:
```bash
cp .env.example .env
```

Or on Windows:
```powershell
Copy-Item .env.example .env
```

### Step 2: Add your API keys

Open `.env` and add your keys:

**Option A: Using OpenAI (Recommended)**
```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4
```

**Option B: Using Anthropic**
```env
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

### Step 3: Run the server

```bash
cd backend
python run.py
```

The server will start at: **http://localhost:8000**

### Step 4: Test the API

Visit the interactive docs at: **http://localhost:8000/docs**

Or test with curl:
```bash
curl -X POST "http://localhost:8000/api/tourism/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "I am going to Bangalore, what is the temperature there?"}'
```

## Need API Keys?

- **OpenAI**: Sign up at https://platform.openai.com/
- **Anthropic**: Sign up at https://console.anthropic.com/

## Troubleshooting

If you see "OPENAI_API_KEY not set", make sure:
1. You created the `.env` file in the root directory (not in backend/)
2. You added your API key without quotes
3. You restarted the server after creating .env
