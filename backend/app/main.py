from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes.tourism_routes import router as tourism_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the application's startup and shutdown logic.
    """
    print("Application startup...")
    print("Initializing Tourism AI Agent system...")
    yield 
    print("Application shutdown...")

app = FastAPI(
    title="Multi-Agent Tourism API",
    description="An AI-powered tourism assistant using multi-agent architecture",
    version="1.0.0",
    lifespan=lifespan 
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tourism_router)

@app.get("/", tags=["Health Check"])
def read_root():
    """Root endpoint to check if the API is running."""
    return {
        "status": "ok",
        "message": "Welcome to the Multi-Agent Tourism API!",
        "docs": "/docs",
        "version": "1.0.0"
    }