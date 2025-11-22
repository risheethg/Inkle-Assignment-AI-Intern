# Multi-Agent Tourism API - Backend

AI-powered tourism assistant using multi-agent architecture with FastAPI.

## Features

- **Parent Tourism Agent**: Orchestrates the entire system
- **Weather Agent**: Fetches real-time weather data from Open-Meteo API
- **Places Agent**: Discovers tourist attractions using Overpass API (OpenStreetMap)
- **AI Integration**: Supports OpenAI and Anthropic for natural language processing

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Choose your AI provider: openai or anthropic
AI_PROVIDER=openai

# OpenAI Configuration (if using OpenAI)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# Anthropic Configuration (if using Anthropic)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Application Settings
LOG_LEVEL=20
```

### 3. Run the Backend

```bash
# From the backend directory
python run.py
```

Or using uvicorn directly:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### POST /api/tourism/chat
Main chatbot endpoint for tourism queries.

**Request:**
```json
{
  "query": "I'm going to Bangalore, what is the temperature there?"
}
```

**Response:**
```json
{
  "location": "Bangalore",
  "weather_info": "In Bangalore it's currently 24°C with a chance of 35% to rain.",
  "places_info": null,
  "final_response": "In Bangalore it's currently 24°C with a chance of 35% to rain."
}
```

### GET /api/tourism/health
Check service health and active agents.

### GET /
Root health check endpoint.

## Example Queries

1. **Weather Query:**
   ```
   "I'm going to Bangalore, what is the temperature there?"
   ```

2. **Places Query:**
   ```
   "I'm going to Paris, let's plan my trip."
   ```

3. **Combined Query:**
   ```
   "What can I do in Tokyo and what's the weather like?"
   ```

## Architecture

```
TourismAgent (Parent)
├── Analyzes user query using AI
├── Validates location using Nominatim Geocoding API
├── Delegates to child agents:
│   ├── WeatherAgent → Open-Meteo API
│   └── PlacesAgent → Overpass API (OpenStreetMap)
└── Combines results into natural language response
```

## Project Structure

```
backend/
├── app/
│   ├── core/
│   │   ├── config.py       # Configuration settings
│   │   └── logger.py       # Logging setup
│   ├── models/
│   │   ├── agent_models.py # Agent request/response models
│   │   ├── location_models.py
│   │   └── weather_models.py
│   ├── repos/
│   │   ├── geo_repo.py     # Geocoding repository
│   │   ├── places_repo.py  # Places repository
│   │   └── weather_repo.py # Weather repository
│   ├── routes/
│   │   └── tourism_routes.py # API routes
│   ├── services/
│   │   ├── ai_client.py    # AI provider wrapper
│   │   ├── tourism_agent.py # Parent agent
│   │   ├── weather_agent.py # Weather child agent
│   │   └── places_agent.py  # Places child agent
│   └── main.py             # FastAPI application
├── requirements.txt
└── run.py
```

## Technologies Used

- **FastAPI**: Modern web framework
- **OpenAI / Anthropic**: AI language models
- **Open-Meteo API**: Weather data
- **Nominatim API**: Geocoding
- **Overpass API**: Tourist attractions from OpenStreetMap
- **Pydantic**: Data validation
- **httpx**: Async HTTP client

## Error Handling

The system handles:
- Non-existent places: Returns a message that the place couldn't be found
- API failures: Graceful degradation with fallback responses
- Network errors: Proper error logging and user-friendly messages
