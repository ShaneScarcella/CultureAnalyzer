import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List

def get_match_scores(
    text_embedding: np.ndarray,
    profile_embeddings: Dict[str, np.ndarray],
    top_n: int
) -> List[Dict]:
    """
    Calculates cosine similarity between a text embedding and profile embeddings.

    Args:
        text_embedding: The embedding of the user's input text.
        profile_embeddings: A dictionary of {profile_name: embedding}.
        top_n: The number of top matches to return.

    Returns:
        A list of dictionaries, sorted by score, each containing "name" and "score".
    """
    if not profile_embeddings:
        return []

    # Reshape user text embedding to 2D - needed for comparison
    text_embedding_reshaped = text_embedding.reshape(1, -1)

    profile_names = list(profile_embeddings.keys())
    profile_vectors = np.array(list(profile_embeddings.values()))

    # Calculate similarity scores
    cosine_scores = cosine_similarity(text_embedding_reshaped, profile_vectors)[0]

    results = [
        {"name": name, "score": round(float(score), 4)}
        for name, score in zip(profile_names, cosine_scores)
    ]

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
    
    return sorted_results[:top_n]