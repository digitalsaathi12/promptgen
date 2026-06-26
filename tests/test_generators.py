import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_list_and_get_generators(client: AsyncClient, user_headers):
    # List active generators
    resp = await client.get("/api/v1/generators/", headers=user_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 3 # instagram_reel, hook_generator, script_generator, etc.
    assert any(g["id"] == "instagram_reel" for g in data)

    # Get single generator config
    resp_detail = await client.get("/api/v1/generators/instagram_reel", headers=user_headers)
    assert resp_detail.status_code == 200
    assert resp_detail.json()["label"] == "Instagram Reel Generator"

@pytest.mark.asyncio
async def test_generate_content_validation_and_parsing(client: AsyncClient, user_headers):
    # 1. Valid execution payload
    payload = {
        "payload": {
            "business_name": "Balaji Sweets",
            "industry": "Food & Beverage",
            "platform": "Instagram",
            "language": "Hinglish",
            "tone": "Casual"
        },
        "model_name": "auto"
    }
    resp = await client.post("/api/v1/generators/instagram_reel/generate", json=payload, headers=user_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "constructed_prompt" in data
    assert "ai_model" in data
    # Output must have expected keys: hook, intro, body, cta, caption
    assert "output" in data
    assert "hook" in data["output"]
    assert "caption" in data["output"]

    # 2. Invalid validation payload (missing required field: industry)
    invalid_payload = {
        "payload": {
            "business_name": "Balaji Sweets"
            # industry missing
        }
    }
    resp_invalid = await client.post("/api/v1/generators/instagram_reel/generate", json=invalid_payload, headers=user_headers)
    assert resp_invalid.status_code == 422
    assert "required" in resp_invalid.json()["error"]["message"]
