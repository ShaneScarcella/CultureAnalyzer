import numpy as np
from sentence_transformers import SentenceTransformer
from typing import Dict

from app.data.culture_profiles import PREDEFINED_PROFILES

model = SentenceTransformer('all-MiniLM-L6-v2')

# Precompute profile embeddings once at startup, turns each into a vector representation

EMBEDDED_PROFILES: Dict[str, Dict[str, np.ndarray]] = {
    "culture": {
        name: model.encode(description)
        for name, description in PREDEFINED_PROFILES["culture"].items()
    },
    "role": {
        name: model.encode(description)
        for name, description in PREDEFINED_PROFILES["role"].items()
    },
    "skills": {
        name: model.encode(description)
        for name, description in PREDEFINED_PROFILES["skills"].items()
    }
}