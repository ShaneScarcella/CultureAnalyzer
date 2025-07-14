from fastapi import FastAPI
from app.api.v1.endpoints import analysis
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Culture Fit & Role Match Analyzer Backend",
    description="AI-powered service to analyze text for company culture and tech-role fit."
)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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