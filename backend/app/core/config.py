from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Tourism Intern"
    VERSION: str = "1.0.0"
    
    LOGGER: int = int(os.getenv("LOG_LEVEL", "20"))

    # External API URLs
    NOMINATIM_URL: str = "https://nominatim.openstreetmap.org/search"
    OPEN_METEO_URL: str = "https://api.open-meteo.com/v1/forecast"
    OVERPASS_URL: str = "https://overpass-api.de/api/interpreter"

    # AI Configuration
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "openai")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")

    class Config:
        case_sensitive = True

settings = Settings()