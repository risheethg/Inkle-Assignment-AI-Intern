from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (2 levels up from this file)
env_path = Path(__file__).resolve().parent.parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
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
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    class Config:
        case_sensitive = True

settings = Settings()