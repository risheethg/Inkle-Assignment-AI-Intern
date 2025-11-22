class Settings:
    PROJECT_NAME: str = "AI Tourism Intern"
    VERSION: str = "1.0.0"
    
    LOGGER: int = 20

    NOMINATIM_URL: str = "https://nominatim.openstreetmap.org/search"
    OPEN_METEO_URL: str = "https://api.open-meteo.com/v1/forecast"
    OVERPASS_URL: str = "https://overpass-api.de/api/interpreter"

settings = Settings()