from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

from .culture_profiles import PREDEFINED_PROFILES

app = FastAPI(
    title = "Culture Fit & Role Match Analyzer Backend",
    description = "AI-powered service to analyze text for company culture and tech-role fit."
)

