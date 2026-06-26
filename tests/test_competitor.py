import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_competitor_analysis_and_history(client: AsyncClient, user_headers):
    # Perform website analysis
    payload = {"website": "example.com"}
    resp = await client.post("/api/v1/competitor/analyze", json=payload, headers=user_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "seo_score" in data
    assert "keywords" in data
    assert "social_presence" in data
    assert len(data["strengths"]) >= 1

    # Fetch History
    hist_resp = await client.get("/api/v1/competitor/history", headers=user_headers)
    assert hist_resp.status_code == 200
    hist_data = hist_resp.json()
    assert len(hist_data) >= 1
    assert hist_data[0]["website"] == "example.com"
