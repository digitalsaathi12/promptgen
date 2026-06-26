import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_search_location_and_history(client: AsyncClient, user_headers):
    # Perform Search
    payload = {"query": "Dentist in Indore"}
    resp = await client.post("/api/v1/location/search", json=payload, headers=user_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 1
    assert "business_name" in data[0]
    assert "coordinates" in data[0]
    assert "gmaps_link" in data[0]
    assert len(data[0]["nearby_competitors"]) >= 1

    # Fetch History
    hist_resp = await client.get("/api/v1/location/history", headers=user_headers)
    assert hist_resp.status_code == 200
    hist_data = hist_resp.json()
    assert len(hist_data) >= 1
    assert hist_data[0]["query"] == "Dentist in Indore"
