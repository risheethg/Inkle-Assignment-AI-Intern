# TravelMate AI - Multi-Agent Tourism Assistant

An intelligent AI-powered tourism chatbot built with a multi-agent architecture using LangGraph. Get real-time weather information, discover tourist attractions, and receive personalized travel itineraries with transparent reasoning and interactive UI.

##  Live Demo

- **Frontend**: [https://inkle-assignment-ai-intern-nu.vercel.app](https://inkle-assignment-ai-intern-nu.vercel.app)
- **Backend API**: [https://inkle-assignment-ai-intern-5pk5.onrender.com](https://inkle-assignment-ai-intern-5pk5.onrender.com)
- **API Documentation**: [https://inkle-assignment-ai-intern-5pk5.onrender.com/docs](https://inkle-assignment-ai-intern-5pk5.onrender.com/docs)

> **Note**: The backend is hosted on Render's free tier, which spins down after 15 minutes of inactivity. The first request after inactivity may take 30-50 seconds to wake up the service.

## Project Overview

This project implements an **Advanced Multi-Agent Architecture with LangGraph** where:
- **Parent Agent (Tourism AI)**: Orchestrates the system using LangGraph workflow, analyzes user queries, and coordinates child agents
- **Weather Agent**: Fetches real-time weather data using Open-Meteo API
- **Places Agent**: Discovers tourist attractions using Overpass API (OpenStreetMap)
- **Query Analyzer**: Intelligently categorizes queries and determines execution strategy
- **Response Synthesizer**: Generates contextual responses with proactive suggestions

All agents use AI (OpenAI/Anthropic/Gemini) for natural language understanding and response generation with streaming support.

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework with SSE streaming
- **Python 3.12+**: Core language
- **LangGraph**: State machine for agent orchestration
- **OpenAI/Anthropic/Gemini**: AI language models with multi-provider support
- **httpx**: Async HTTP client
- **Pydantic**: Data validation and models

### Frontend
- **React 19**: UI framework with hooks
- **Vite**: Lightning-fast build tool
- **Tailwind CSS**: Utility-first styling
- **Axios**: HTTP client
- **Server-Sent Events (SSE)**: Real-time streaming updates

### External APIs
- **Nominatim API**: Geocoding (place name to coordinates)
- **Open-Meteo API**: Real-time weather data with precipitation
- **Overpass API**: Tourist attractions from OpenStreetMap

##  Features

### Core Capabilities
-  **Multi-Agent LangGraph Architecture**: Coordinated workflow with Query Analyzer, Trip Planner, Weather Agent, Places Agent, and Response Generator
-  **Natural Language Understanding**: Intelligently parses complex travel queries with context awareness
-  **Real-time Weather Data**: Current temperature and precipitation probability
-  **Tourist Attractions Discovery**: Up to 5 curated recommendations per location
-  **Multi-Day Itinerary Planning**: Automatic day-by-day trip planning with morning/afternoon/evening activities
-  **Conversational Memory**: Maintains context across multiple queries in a session
-  **Smart Query Classification**: Distinguishes between information requests, place lists, and trip planning

### Advanced Features
-  **Real-time Streaming**: Live agent reasoning with animated thinking display (Gemini-style)
-  **Proactive Suggestions**: Context-aware follow-up suggestions after each response
-  **Interactive UI Components**: 
  - Expandable place cards with "Learn More" buttons
  - Weather cards with collapsible details
  - Location cards with "Explore More" actions
  - Animated suggestion buttons
-  **Context Preservation**: Maintains main location when exploring specific attractions
-  **Copy to Clipboard**: One-click response copying
-  **Dynamic Response Formatting**: Automatically switches between formats (simple, detailed places, multi-step itinerary)
-  **Transparent Reasoning**: See which agents ran and why in an expandable dropdown
-  **Full-Screen Responsive Design**: Adapts perfectly to any screen size

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- Docker & Docker Compose (optional, for containerized deployment)
- OpenAI, Anthropic, or Gemini API key

### 1. Clone the Repository

```bash
git clone https://github.com/risheethg/Inkle-Assignment-AI-Intern.git
cd Inkle-Assignment-AI-Intern
```

### 2. Setup Environment Variables

Create a `.env` file in the root directory:

```env
# AI Provider Configuration (choose one)
AI_PROVIDER=gemini  # Options: openai, anthropic, gemini

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# Anthropic Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Gemini Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash-exp

# Logging
LOG_LEVEL=20
```

### 3. Docker Deployment (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d
```

Access the application at: http://localhost:5173

### 4. Manual Setup (Alternative)

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python run.py
```
Backend runs at: http://localhost:8000

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at: http://localhost:5173

### 5. Test the Application

Visit http://localhost:5173 and try:
- **Simple Query**: "What's the weather in Tokyo?"
- **Places Query**: "What are the best places to visit in Paris?"
- **Multi-Day Trip**: "Plan a 3-day trip to Bali"
- **Information Request**: "Tell me more about Tokyo Tower" (after getting places in Tokyo)
- **Follow-up**: Click on suggestion buttons for contextual queries

##  Example Interactions

**Example 1: Simple Weather Query**
```
User: What's the weather in Tokyo?
AI: [Shows thinking process with Query Analyzer and Weather Agent]
    You're asking about the weather at the Tokyo! It's currently a pleasant 21.2C there, 
    with a very low 1.0% chance of rain. Sounds like perfect weather!
    
     Location: Tokyo
     Weather: Currently 21.2C with 1.0% chance of rain
    
     Suggestions:
    - Check current weather in Tokyo
    - Find best restaurants in Tokyo
```

**Example 2: Places Discovery**
```
User: Best places in Tokyo?
AI: [Shows reasoning: Query Analyzer  Places Agent  Response Generator]
    Here are the top attractions in Tokyo:
    
     Top Attractions (5 places)
    1. Tokyo Tower  [Click to expand and "Learn More"]
    2. Senso-ji Temple 
    3. Meiji Shrine 
    4. Tokyo Skytree 
    5. Imperial Palace 
    
     You might also want to:
    1. Check current weather in Tokyo 
    2. Get accommodation tips 
```

**Example 3: Multi-Day Trip Planning**
```
User: Plan a 3-day trip to Bali
AI: [Streaming reasoning shows: Query Analyzer  Trip Planner  Weather Agent  Places Agent]
    
     Your 3-Day Bali Itinerary
    
     Day 1: Cultural Immersion
     Morning:
    - Tanah Lot Temple (8:00 AM - 11:00 AM)
      [Iconic sea temple, best at sunrise]
    
     Afternoon:
    - Ubud Monkey Forest (2:00 PM - 5:00 PM)
      [Sacred sanctuary with playful monkeys]
    
     Evening:
    - Traditional Kecak Dance at Uluwatu (6:00 PM - 8:00 PM)
    
    [Day 2 and Day 3 continue with similar structure...]
    
     Weather: Currently 28C with 15% chance of rain
    
     Suggestions:
    - Find best restaurants in Bali
    - Get accommodation tips
```

**Example 4: Follow-up Question (Context Preserved)**
```
[After getting places in Tokyo]
User: [Clicks "Learn More" on Tokyo Tower]
AI: [Query correctly interpreted as information request about specific attraction]
    
    Tokyo Tower is an iconic landmark standing at 333 meters tall. 
    
     Details:
     Opening Hours: 9:00 AM - 11:00 PM
     Entry Fee: 1,200 for Main Deck
     Best Time: Evening for city lights view
     Tips: Visit on weekdays to avoid crowds
    
     Location: Tokyo [Preserved - still shows main city, not "Tokyo Tower"]
```

## Project Structure

```
.
 backend/
    app/
       core/
          config.py          # Multi-provider AI configuration
          logger.py          # Logging setup
       models/
          agent_models.py    # Request/Response models, ReasoningStep, ProactiveSuggestion
          base_models.py     # Core data models
          location_models.py # Geocoding models
          weather_models.py  # Weather data models
       repos/
          geo_repo.py        # Nominatim API integration
          weather_repo.py    # Open-Meteo API integration
          places_repo.py     # Overpass API integration
       routes/
          tourism_routes.py  # FastAPI routes with SSE streaming
       services/
          ai_client.py       # Multi-provider AI client (OpenAI/Anthropic/Gemini)
          langgraph_tourism.py # LangGraph orchestration with state management
          weather_agent.py   # Weather data agent
          places_agent.py    # Tourist attractions agent
       main.py                # FastAPI app initialization
    Dockerfile
    requirements.txt
    run.py
    README.md
 frontend/
    src/
       components/
          ChatInterface.jsx       # Main chat component with SSE
          MessageBubble.jsx       # Message display with interactive elements
          LoadingDots.jsx         # Animated loading with status messages
          ThinkingDropdown.jsx    # Real-time reasoning display
          InteractivePlace.jsx    # Expandable place cards
          WeatherCard.jsx         # Interactive weather display
          LocationCard.jsx        # Location display with actions
       App.jsx                     # Main app layout
       main.jsx                    # React entry point
       index.css                   # Global styles and animations
    Dockerfile
    nginx.conf
    package.json
    README.md
 docker-compose.yml
 .env.example
 .gitignore
 QUICKSTART.md
 TESTING_GUIDE.md
 README.md
```

##  Architecture

### LangGraph Multi-Agent Workflow

```
                         User Query
                              |
                              v
                    
                     Query Analyzer    Classifies intent & extracts location
                         Node             Preserves main_location context
                    
                             |
                             v
                    
                      Trip Planner     Determines response format
                         Node             (simple/detailed_places/multi_step_itinerary)
                    
                             |
              
              v                             v
         [needs_weather?]            [needs_places?]
              |                             |
              v                             v
                    
      Weather Agent               Places Agent  
          Node                        Node      
                    
             |                             |
             v                             v
       Open-Meteo API              Overpass API
             |                             |
             
                            v
                  
                  Response Generator  Synthesizes final response
                        Node             Generates proactive suggestions
                       Streams reasoning via SSE
                            |
                            v
                    JSON Response with:
                    - final_response
                    - location & main_location
                    - weather_info
                    - places_info
                    - reasoning_trace
                    - suggestions[]
```

### State Management

```python
TourismState:
  - query: str                          # Current user query
  - conversation_history: list[dict]    # Session memory
  - location: str                       # Specific location/attraction
  - main_location: str                  # Primary city (preserved)
  - needs_weather: bool                 # Weather data needed
  - needs_places: bool                  # Places data needed
  - query_type: str                     # Response format type
  - is_complex_query: bool              # Multi-step planning
  - weather_info: str                   # Weather result
  - places_info: list[str]              # Attractions result
  - reasoning_trace: list[dict]         # Agent execution log
  - final_response: str                 # Generated response
```

### Real-time Streaming Flow

```
Frontend (EventSource) SSE Backend (FastAPI)
                                     
           1. User sends query       
         
                                     
           2. Stream reasoning       
         
           {"type":"reasoning",      
            "data":{agent, action}}  
                                     
           3. Stream reasoning       
         
           (repeated for each node)  
                                     
           4. Stream final response  
         
           {"type":"complete",       
            "data":{...response}}    
```

##  API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

#### 1. **POST /api/tourism/chat** (Standard)

Standard request-response endpoint.

Request:
```json
{
  "query": "What's the weather in Paris?",
  "conversation_history": [
    {"role": "user", "content": "Previous query"},
    {"role": "assistant", "content": "Previous response"}
  ]
}
```

Response:
```json
{
  "location": "Paris",
  "weather_info": "Currently 15C with 20% chance of rain",
  "places_info": null,
  "final_response": "In Paris it's currently 15C with a chance of 20% to rain.",
  "reasoning_trace": [
    {
      "agent": "Query Analyzer",
      "action": "Analyzing user query",
      "reason": "Understanding what information the user needs"
    }
  ],
  "suggestions": [
    {
      "text": " Find best attractions in Paris",
      "query": "What are the top tourist attractions in Paris?"
    }
  ],
  "conversation_history": [...]
}
```

#### 2. **POST /api/tourism/chat/stream** (SSE Streaming)

Real-time streaming endpoint with live reasoning updates.

Request: Same as above

Response Stream:
```
data: {"type":"reasoning","data":{"agent":"Query Analyzer","action":"Analyzing user query","reason":"..."}}

data: {"type":"reasoning","data":{"agent":"Weather Agent","action":"Fetching weather data","reason":"..."}}

data: {"type":"complete","data":{...full response object...}}
```

#### 3. **GET /api/tourism/health**

Health check endpoint.

Response:
```json
{
  "status": "healthy",
  "service": "Tourism AI Agent"
}
```

##  Development

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

# Start dev server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Docker Development

```bash
# Build images
docker-compose build

# Start services
docker-compose up

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild without cache
docker-compose build --no-cache
```

### Environment Variables

| Variable | Description | Default | Options |
|----------|-------------|---------|---------|
| `AI_PROVIDER` | AI model provider | `openai` | `openai`, `anthropic`, `gemini` |
| `OPENAI_API_KEY` | OpenAI API key | - | Required if using OpenAI |
| `OPENAI_MODEL` | OpenAI model | `gpt-4` | `gpt-4`, `gpt-3.5-turbo` |
| `ANTHROPIC_API_KEY` | Anthropic API key | - | Required if using Anthropic |
| `ANTHROPIC_MODEL` | Anthropic model | `claude-3-sonnet-20240229` | Any Claude model |
| `GEMINI_API_KEY` | Google Gemini API key | - | Required if using Gemini |
| `GEMINI_MODEL` | Gemini model | `gemini-2.0-flash-exp` | `gemini-2.0-flash-exp`, `gemini-1.5-flash` |
| `LOG_LEVEL` | Logging level | `20` | `10` (DEBUG), `20` (INFO), `30` (WARNING) |

##  Key Implementation Highlights

### 1. LangGraph State Machine
- Implements a directed acyclic graph (DAG) for agent coordination
- Each node represents a specific agent task
- Conditional edges route execution based on state
- Built-in error handling and recovery

### 2. Context-Aware Query Processing
- Distinguishes between cities and specific attractions
- Preserves `main_location` across follow-up queries
- Detects information requests vs. trip planning queries
- Handles ambiguous references ("it", "there", "that place")

### 3. Dynamic Response Formatting
Three distinct response formats automatically selected:
- **Simple**: Conversational responses for general queries
- **Detailed Places**: Structured list with interactive cards
- **Multi-Step Itinerary**: Day-by-day plans with time slots

### 4. Real-time Streaming Architecture
- Server-Sent Events (SSE) for live updates
- Asynchronous callbacks for reasoning propagation
- Non-blocking execution with asyncio
- Efficient state management during streaming

### 5. Interactive Frontend Components
- Expandable place cards with lazy-loaded details
- Animated reasoning dropdown with Gemini-style display
- Click-to-query suggestion buttons
- Auto-scrolling chat interface
- Full-screen responsive design

##  Testing

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for detailed testing procedures.

Quick test commands:
```bash
# Backend API test
curl -X POST http://localhost:8000/api/tourism/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Weather in Tokyo?"}'

# Health check
curl http://localhost:8000/api/tourism/health
```

##  Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

##  Troubleshooting

### Common Issues

**Backend not starting:**
- Check if port 8000 is available
- Verify API keys in `.env` file
- Ensure Python 3.12+ is installed
- Check Docker logs: `docker-compose logs backend`

**Frontend build errors:**
- Clear node_modules: `rm -rf node_modules && npm install`
- Check Node.js version: `node --version` (should be 18+)
- Verify Vite port 5173 is available

**SSE streaming not working:**
- Check browser console for connection errors
- Verify CORS settings in FastAPI
- Ensure backend `/chat/stream` endpoint is accessible

**Places not showing:**
- Verify Overpass API is accessible
- Check if location has sufficient OSM data
- Review backend logs for API errors

For detailed troubleshooting, see [TESTING_GUIDE.md](TESTING_GUIDE.md).

##  Performance Considerations

- **Async/Await**: All I/O operations are asynchronous for better concurrency
- **Connection Pooling**: httpx client reuses connections to external APIs
- **Streaming**: Reduces time-to-first-byte for better UX
- **Caching**: Browser caching for static frontend assets
- **Error Recovery**: Graceful degradation when APIs fail
- **Rate Limiting**: Respects external API rate limits

##  Future Enhancements

- [ ] User authentication and saved itineraries
- [ ] Image generation for destinations using DALL-E/Stable Diffusion
- [ ] Real-time pricing for attractions
- [ ] Integration with booking APIs (hotels, flights)
- [ ] Multi-language support
- [ ] Voice input/output with speech recognition
- [ ] Mobile app (React Native)
- [ ] Offline mode with cached data
- [ ] Social sharing of itineraries
- [ ] Collaborative trip planning

##  Deployment

### Production Deployment

The application is deployed using:
- **Frontend**: Vercel (https://inkle-assignment-ai-intern-nu.vercel.app)
- **Backend**: Render (https://inkle-assignment-ai-intern-5pk5.onrender.com)

### Deployment Guide

For detailed deployment instructions to Vercel and Render, see [DEPLOYMENT.md](DEPLOYMENT.md).

**Quick Deploy:**

1. **Backend (Render)**:
   - Connect your GitHub repo
   - Set environment variables (AI_PROVIDER, API keys)
   - Deploy from `hosting` branch

2. **Frontend (Vercel)**:
   - Connect your GitHub repo
   - Set root directory to `frontend`
   - Add `VITE_API_URL` environment variable
   - Deploy from `hosting` branch

### Free Tier Limitations

- **Render**: Service sleeps after 15 min inactivity (30-50s cold start)
- **Vercel**: 100 GB bandwidth/month
- Consider using [UptimeRobot](https://uptimerobot.com) to keep backend warm

##  License

This project is part of the Inkle AI Intern Assignment.

##  Contact

**Risheeth G**
- GitHub: [@risheethg](https://github.com/risheethg)
- Project: [Inkle-Assignment-AI-Intern](https://github.com/risheethg/Inkle-Assignment-AI-Intern)
- Live Demo: [TravelMate AI](https://inkle-assignment-ai-intern-nu.vercel.app)

##  Acknowledgments

- **LangGraph** by LangChain for state machine orchestration
- **Open-Meteo** for free weather API
- **Vercel** for frontend hosting
- **Render** for backend hosting
- **OpenStreetMap** and **Overpass API** for location data
- **FastAPI** for excellent async web framework
- **React** and **Vite** for modern frontend tooling

---

Made with  for Inkle AI Intern Assignment
