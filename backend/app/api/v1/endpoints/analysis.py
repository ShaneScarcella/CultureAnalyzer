from fastapi import APIRouter, UploadFile, File, Depends
from app.core.models import UserTextInput, AnalysisResponse
from app.services.embedding_service import model, EMBEDDED_PROFILES
from app.services.matching_service import get_match_scores
from app.services.file_processing_service import parse_file_text

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_text(user_input: UserTextInput):
    """
    Analyzes the user's input text against predefined profiles.

    This endpoint receives text, generates an embedding for it, and then
    calculates the similarity scores against culture, role, and skill profiles.
    """
    text_embedding = model.encode(user_input.text)

    # Call the matching service to get scores for each profile type
    culture_matches = get_match_scores(
        text_embedding=text_embedding,
        profile_embeddings=EMBEDDED_PROFILES["culture"],
        top_n=user_input.top_n
    )

    role_matches = get_match_scores(
        text_embedding=text_embedding,
        profile_embeddings=EMBEDDED_PROFILES["role"],
        top_n=user_input.top_n
    )

    skill_matches = get_match_scores(
        text_embedding=text_embedding,
        profile_embeddings=EMBEDDED_PROFILES["skills"],
        top_n=user_input.top_n
    )

    return AnalysisResponse(
        culture_matches=culture_matches,
        role_matches=role_matches,
        skill_matches=skill_matches
    )


@router.post("/analyze-file", response_model=AnalysisResponse)
async def analyze_file(
    top_n: int = 5,
    file: UploadFile = File(...)
):
    """
    Parses an uploaded file (PDF or DOCX), analyzes its text, 
    and returns similarity scores against predefined profiles.
    """

    extracted_text = await parse_file_text(file)
    
    text_embedding = model.encode(extracted_text)

    culture_matches = get_match_scores(
        text_embedding=text_embedding,
        profile_embeddings=EMBEDDED_PROFILES["culture"],
        top_n=top_n
    )

    role_matches = get_match_scores(
        text_embedding=text_embedding,
        profile_embeddings=EMBEDDED_PROFILES["role"],
        top_n=top_n
    )

    skill_matches = get_match_scores(
        text_embedding=text_embedding,
        profile_embeddings=EMBEDDED_PROFILES["skills"],
        top_n=top_n
    )

    return AnalysisResponse(
        culture_matches=culture_matches,
        role_matches=role_matches,
        skill_matches=skill_matches
    )