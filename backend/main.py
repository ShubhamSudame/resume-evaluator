from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Import routes
from routes import job_descriptions, resumes, evaluations

# Load environment variables
# Try to load from parent directory first (for Docker), then current directory
load_dotenv("../.env")
load_dotenv(".env")  # Fallback to current directory

# Get environment mode
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

app = FastAPI(
    title="Resume Evaluator API",
    description="A comprehensive API for resume evaluation and job description management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    debug=DEBUG
)

# Configure CORS for frontend integration
if ENVIRONMENT == "development":
    # Development: Allow Angular dev server
    allowed_origins = [
        "http://localhost:4200",  # Angular default dev port
        "http://localhost:3000",  # Alternative dev port
        "http://127.0.0.1:4200",
        "http://127.0.0.1:3000"
    ]
else:
    # Production: Only allow specific origins
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:4200").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(job_descriptions.router)
app.include_router(resumes.router)
app.include_router(evaluations.router)

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Resume Evaluator API is running",
        "version": "1.0.0",
        "environment": ENVIRONMENT,
        "debug": DEBUG
    }

@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "name": "Resume Evaluator API",
        "version": "1.0.0",
        "environment": ENVIRONMENT,
        "description": "A comprehensive API for resume evaluation and job description management",
        "endpoints": {
            "job_descriptions": "/api/job-descriptions",
            "resumes": "/api/resumes",
            "evaluations": "/api/evaluations",
            "docs": "/docs",
            "health": "/api/health"
        }
    }

if __name__ == "__main__":
    import uvicorn
    print(f"Starting Resume Evaluator API in {ENVIRONMENT} mode...")
    print(f"Debug mode: {DEBUG}")
    print(f"Allowed origins: {allowed_origins}")
    uvicorn.run(app, host="0.0.0.0", port=8000) 