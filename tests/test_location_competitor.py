import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_location_intelligence_flow(client: AsyncClient, user_headers):
    # Post search
    payload = {
        "country": "India",
        "state": "Madhya Pradesh",
        "city": "Indore",
        "area": "Vijay Nagar",
        "category": "dentist",
        "radius": 1500,
        "limit": 3
    }
    resp = await client.post("/api/v1/location-intelligence/search", json=payload, headers=user_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 1
    assert "business_name" in data[0]
    assert "nearby_competitors" in data[0]

    # Get history
    resp_hist = await client.get("/api/v1/location-intelligence/history", headers=user_headers)
    assert resp_hist.status_code == 200
    assert len(resp_hist.json()) >= 1
    assert resp_hist.json()[0]["city"] == "Indore"

@pytest.mark.asyncio
async def test_competitor_analysis_flow(client: AsyncClient, user_headers):
    # Post scraping evaluation
    payload = {
        "website": "example.com",
        "business_name": "Example Corp"
    }
    resp = await client.post("/api/v1/competitor-analysis/analyze", json=payload, headers=user_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "seo_score" in data
    assert "keywords" in data
    assert "social_presence" in data

    # Get reports
    resp_reps = await client.get("/api/v1/competitor-analysis/reports", headers=user_headers)
    assert resp_reps.status_code == 200
    assert len(resp_reps.json()) >= 1
    assert resp_reps.json()[0]["website_url"] == "example.com"
