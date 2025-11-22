# Full Stack Testing Guide

This guide will help you test the complete Tourism AI Assistant application.

## Prerequisites

1. Python 3.12+ installed
2. Node.js 18+ installed
3. API key for OpenAI or Anthropic

## Step 1: Setup Backend

### Create .env file

In the root directory, create a `.env` file:

```env
AI_PROVIDER=openai
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4
LOG_LEVEL=20
```

### Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Test backend imports

```bash
python test_imports.py
```

You should see all checks passing.

### Start backend server

```bash
python run.py
```

Backend should be running at: http://localhost:8000

Visit http://localhost:8000/docs to see the API documentation.

## Step 2: Setup Frontend

Open a new terminal window.

### Install frontend dependencies

```bash
cd frontend
npm install
```

### Start frontend dev server

```bash
npm run dev
```

Frontend should be running at: http://localhost:5173

## Step 3: Test the Application

1. Open http://localhost:5173 in your browser
2. You should see the Tourism AI Assistant interface
3. Try these test queries:

### Test 1: Weather Only
```
What's the weather in Bangalore?
```

Expected: Response with temperature and precipitation probability

### Test 2: Places Only
```
I'm going to Paris, let's plan my trip
```

Expected: List of 5 tourist attractions in Paris

### Test 3: Combined Query
```
I'm going to Tokyo, what's the weather and what can I visit?
```

Expected: Weather information + list of tourist attractions

### Test 4: Non-existent Place
```
What's the weather in Atlantis?
```

Expected: Error message stating the place doesn't exist

## Troubleshooting

### Backend Issues

**Error: "OPENAI_API_KEY not set"**
- Make sure .env file exists in root directory
- Check that API key is set correctly
- Restart the backend server

**Error: "Module not found"**
- Run: `pip install -r requirements.txt`
- Make sure you're in the backend directory

**Port 8000 already in use**
- Stop other processes using port 8000
- Or change port in `backend/run.py`

### Frontend Issues

**Error: "Network Error"**
- Make sure backend is running on http://localhost:8000
- Check CORS settings in backend
- Open browser console for detailed errors

**Blank page**
- Open browser console (F12) for errors
- Make sure all npm dependencies are installed
- Try: `npm install` then `npm run dev`

**Styles not working**
- Make sure Tailwind is installed: `npm install -D tailwindcss postcss autoprefixer`
- Check that `tailwind.config.js` and `postcss.config.js` exist

## API Testing with curl

You can also test the backend API directly:

```bash
curl -X POST "http://localhost:8000/api/tourism/chat" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"What's the weather in London?\"}"
```

## Architecture Overview

```
User Browser (localhost:5173)
    |
    | HTTP Request
    v
React Frontend
    |
    | Axios POST /api/tourism/chat
    v
FastAPI Backend (localhost:8000)
    |
    v
Tourism Agent (Parent)
    |
    +---> Weather Agent ---> Open-Meteo API
    |
    +---> Places Agent ---> Overpass API
    |
    +---> AI Client ---> OpenAI/Anthropic API
```

## Next Steps

Once everything is working:
1. Merge feature branches to main
2. Deploy backend (Railway, Render, or AWS)
3. Deploy frontend (Vercel, Netlify, or AWS)
4. Update frontend API_BASE_URL to production backend URL
