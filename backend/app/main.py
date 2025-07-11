from fastapi import FastAPI
from app.api.v1.endpoints import analysis

app = FastAPI(
    title="Culture Fit & Role Match Analyzer Backend",
    description="AI-powered service to analyze text for company culture and tech-role fit."
)

# Include the router from the analysis endpoint file
app.include_router(
    analysis.router, 
    prefix="/api/v1", 
    tags=["Analysis"]
)

@app.get("/")
async def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "Welcome to the Culture & Role Match Analyzer API"}