import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_history_and_favorites_flow(client: AsyncClient, user_headers):
    # 1. Trigger history generation by running a generator
    payload = {
        "payload": {
            "business_name": "Vijay Cafeteria",
            "industry": "Restaurant",
            "platform": "Instagram",
            "language": "English",
            "tone": "Casual"
        }
    }
    await client.post("/api/v1/generators/instagram_reel/generate", json=payload, headers=user_headers)

    # 2. Query history list
    hist_resp = await client.get("/api/v1/history/", headers=user_headers)
    assert hist_resp.status_code == 200
    hist_data = hist_resp.json()
    assert len(hist_data) >= 1
    h_id = hist_data[0]["id"]

    # Query history detail
    detail_resp = await client.get(f"/api/v1/history/{h_id}", headers=user_headers)
    assert detail_resp.status_code == 200
    assert detail_resp.json()["id"] == h_id

    # 3. Create Favorite bookmark
    fav_resp = await client.post(f"/api/v1/favorites/{h_id}", headers=user_headers)
    assert fav_resp.status_code == 201

    # Get Favorites list
    favs_list = await client.get("/api/v1/favorites/", headers=user_headers)
    assert favs_list.status_code == 200
    assert len(favs_list.json()) >= 1
    f_id = favs_list.json()[0]["id"]

    # Delete Favorite
    del_fav = await client.delete(f"/api/v1/favorites/{f_id}", headers=user_headers)
    assert del_fav.status_code == 200
