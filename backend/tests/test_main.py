import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
async def async_client():
    """Create an async client to test the API."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

async def test_read_root(async_client: AsyncClient):
    """Test that the root endpoint returns a successful response and correct message."""
    response = await async_client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Culture & Role Match Analyzer API"}

async def test_analyze_text(async_client: AsyncClient):
    """Test the main text analysis endpoint."""
    test_payload = {
        "text": "I am a Python developer who loves building APIs in agile, startup environments.",
        "top_n": 2
    }
    
    response = await async_client.post("/api/v1/analyze", json=test_payload)
    
    assert response.status_code == 200

    response_data = response.json()
    assert "culture_matches" in response_data
    assert "role_matches" in response_data
    assert "skill_matches" in response_data

    # Number of matches
    assert len(response_data["culture_matches"]) == 2
    
    # Correct keys in JSON
    assert "name" in response_data["culture_matches"][0]
    assert "score" in response_data["culture_matches"][0]