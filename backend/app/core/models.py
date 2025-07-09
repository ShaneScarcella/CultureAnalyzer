from pydantic import BaseModel
from typing import List, Optional

class MatchResult(BaseModel):
    """Model for a single match result, containing name and score."""
    name: str
    score: float

class UserTextInput(BaseModel):
    """Model for the text input from the user."""
    text: str
    top_n: Optional[int] = 5 # Optional: How many top matches to return?

class AnalysisResponse(BaseModel):
    """Model for the final analysis response sent back to the user."""
    culture_matches: List[MatchResult]
    role_matches: List[MatchResult]
    skill_matches: List[MatchResult] # <-- Added this for the new category