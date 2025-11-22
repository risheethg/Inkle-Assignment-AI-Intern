# Multi-Agent Tourism AI Assistant

An AI-powered tourism chatbot built with a multi-agent architecture. Get weather information and tourist attraction recommendations for any location around the world.

## Project Overview

This project implements a **Parent-Child Agent Architecture** where:
- **Parent Agent (Tourism AI)**: Orchestrates the system, analyzes user queries, and coordinates child agents
- **Child Agent 1 (Weather Agent)**: Fetches real-time weather data using Open-Meteo API
- **Child Agent 2 (Places Agent)**: Discovers tourist attractions using Overpass API (OpenStreetMap)

All agents use AI (OpenAI/Anthropic) for natural language understanding and response generation.

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Python 3.12+**: Core language
- **OpenAI/Anthropic**: AI language models
- **httpx**: Async HTTP client
- **Pydantic**: Data validation

### Frontend
- **React 19**: UI framework
- **Vite**: Build tool
- **Tailwind CSS**: Styling
- **Axios**: HTTP client

### External APIs
- **Nominatim API**: Geocoding (place name to coordinates)
- **Open-Meteo API**: Weather data
- **Overpass API**: Tourist attractions from OpenStreetMap

## Features

- Natural language query understanding
- Real-time weather information with precipitation probability
- Up to 5 tourist attraction recommendations
- Error handling for non-existent places
- Clean, modern chat interface
- Responsive design

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- OpenAI or Anthropic API key

### 1. Clone the Repository

```bash
git clone https://github.com/risheethg/Inkle-Assignment-AI-Intern.git
cd Inkle-Assignment-AI-Intern
```

### 2. Setup Environment Variables

Create a `.env` file in the root directory:

```env
AI_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
LOG_LEVEL=20
```

### 3. Start Backend

```bash
cd backend
pip install -r requirements.txt
python run.py
```

Backend runs at: http://localhost:8000

### 4. Start Frontend

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:5173

### 5. Test the Application

Visit http://localhost:5173 and try:
- "What's the weather in Bangalore?"
- "I'm going to Paris, let's plan my trip"
- "Tell me about Tokyo and what's the temperature there"

## Example Interactions

**Example 1: Weather Query**
```
User: I'm going to Bangalore, what is the temperature there?
AI: In Bangalore it's currently 24°C with a chance of 35% to rain.
```

**Example 2: Places Query**
```
User: I'm going to Bangalore, let's plan my trip
AI: In Bangalore these are the places you can go:
- Lalbagh
- Sri Chamarajendra Park
- Bangalore Palace
- Bannerghatta National Park
- Jawaharlal Nehru Planetarium
```

**Example 3: Combined Query**
```
User: I'm going to Bangalore, what is the temperature there? And what are the places I can visit?
AI: In Bangalore it's currently 24°C with a chance of 35% to rain. And these are the places you can go:
- Lalbagh
- Sri Chamarajendra Park
- Bangalore Palace
- Bannerghatta National Park
- Jawaharlal Nehru Planetarium
```

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── core/           # Configuration and logging
│   │   ├── models/         # Pydantic models
│   │   ├── repos/          # API integrations (Geocoding, Weather, Places)
│   │   ├── routes/         # FastAPI routes
│   │   ├── services/       # Agent implementations
│   │   └── main.py         # FastAPI app
│   ├── requirements.txt
│   ├── run.py
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── README.md
├── .env.example
├── .gitignore
├── QUICKSTART.md
├── TESTING_GUIDE.md
└── README.md
```

## Architecture

```
                    User Query
                        |
                        v
              ┌─────────────────┐
              │ Tourism Agent   │ (Parent)
              │   (Orchestrator)│
              └────────┬────────┘
                       |
          ┌────────────┴────────────┐
          v                         v
    ┌──────────┐            ┌──────────┐
    │ Weather  │            │ Places   │
    │  Agent   │            │  Agent   │
    └────┬─────┘            └────┬─────┘
         |                       |
         v                       v
   Open-Meteo API          Overpass API
```

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Main Endpoint

**POST /api/tourism/chat**

Request:
```json
{
  "query": "What's the weather in Paris?"
}
```

Response:
```json
{
  "location": "Paris",
  "weather_info": "In Paris it's currently 15°C with a chance of 20% to rain.",
  "places_info": null,
  "final_response": "In Paris it's currently 15°C with a chance of 20% to rain."
}
```

## Development

### Backend Development

```bash
cd backend
# Install dependencies
pip install -r requirements.txt

# Run tests
python test_imports.py

# Start dev server with auto-reload
python run.py
```

### Frontend Development

```bash
cd frontend
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Troubleshooting

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for detailed troubleshooting steps.

## License

This project is part of the Inkle AI Intern Assignment.

## Contact

Rishee - [@risheethg](https://github.com/risheethg)

Project Link: [https://github.com/risheethg/Inkle-Assignment-AI-Intern](https://github.com/risheethg/Inkle-Assignment-AI-Intern)
