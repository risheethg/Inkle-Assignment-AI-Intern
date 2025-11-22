from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the application's startup and shutdown logic.
    """
    print("Application startup...")
    yield 
    print("Application shutdown...")

app = FastAPI(
    title="PDR to SRS to Jira Automation API",
    description="An API to automate the software requirement lifecycle.",
    version="1.0.0",
    lifespan=lifespan 
)

@app.get("/", tags=["Health Check"])
def read_root():
    """Root endpoint to check if the API is running."""
    return {"status": "ok", "message": "Welcome to the Multi-Agent Tourism API!"}