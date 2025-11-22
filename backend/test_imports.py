# Test script to verify backend functionality
# Run this before starting the server to check for import errors

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

print("Testing imports...")

try:
    from app.core.config import settings
    print("Config loaded")
except Exception as e:
    print(f"Config error: {e}")
    sys.exit(1)

try:
    from app.models.agent_models import UserQuery, AgentResponse
    from app.models.location_models import LocationData
    from app.models.weather_models import WeatherData
    print("Models imported")
except Exception as e:
    print(f"Models error: {e}")
    sys.exit(1)

try:
    from app.repos.geo_repo import GeoRepo
    from app.repos.weather_repo import WeatherRepo
    from app.repos.places_repo import PlacesRepo
    print("Repositories imported")
except Exception as e:
    print(f"Repositories error: {e}")
    sys.exit(1)

try:
    from app.services.ai_client import AIClient
    from app.services.weather_agent import WeatherAgent
    from app.services.places_agent import PlacesAgent
    from app.services.tourism_agent import TourismAgent
    print("Services imported")
except Exception as e:
    print(f"Services error: {e}")
    sys.exit(1)

try:
    from app.routes.tourism_routes import router
    print("Routes imported")
except Exception as e:
    print(f"Routes error: {e}")
    sys.exit(1)

try:
    from app.main import app
    print("FastAPI app imported")
except Exception as e:
    print(f"FastAPI app error: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("All imports successful!")
print("="*50)
print("\nConfiguration:")
print(f"  - AI Provider: {settings.AI_PROVIDER}")
print(f"  - OpenAI Key: {'Set' if settings.OPENAI_API_KEY else 'Not Set'}")
print(f"  - Anthropic Key: {'Set' if settings.ANTHROPIC_API_KEY else 'Not Set'}")
print("\nTo run the server:")
print("  python run.py")
print("\nOr:")
print("  uvicorn app.main:app --reload")
