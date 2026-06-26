import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_list_and_create_templates(client: AsyncClient, admin_headers):
    # Create template
    payload = {
        "title": "Facebook Reel Template",
        "category": "facebook_reel", # mapped as generator_id
        "description": "Generate fb reel scripts",
        "prompt_text": "Act as FB copywriter. Brand: {brand}",
        "tags": "fb,reel"
    }
    resp = await client.post("/api/v1/prompts/", json=payload, headers=admin_headers)
    assert resp.status_code == 201
    assert "id" in resp.json()
    t_id = resp.json()["id"]

    # List templates
    list_resp = await client.get("/api/v1/prompts/", headers=admin_headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 1

    # Delete template
    del_resp = await client.delete(f"/api/v1/prompts/{t_id}", headers=admin_headers)
    assert del_resp.status_code == 200
