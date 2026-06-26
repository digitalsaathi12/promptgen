import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_smart_prompt_generator(client: AsyncClient, user_headers):
    payload = {"text": "Shoe brand ke liye ad banana hai"}
    resp = await client.post("/api/v1/ai/prompt-generator", json=payload, headers=user_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "chatgpt_prompt" in data
    assert "gemini_prompt" in data
    assert "claude_prompt" in data

@pytest.mark.asyncio
async def test_script_generator(client: AsyncClient, user_headers):
    payload = {"topic": "Travel Agency Neemuch", "platform": "reels"}
    resp = await client.post("/api/v1/ai/script-generator", json=payload, headers=user_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "hook" in data
    assert "intro" in data
    assert "body" in data
    assert "cta" in data

@pytest.mark.asyncio
async def test_viral_hooks_generator(client: AsyncClient, user_headers):
    payload = {"topic": "Real Estate Indore"}
    resp = await client.post("/api/v1/ai/viral-hooks", json=payload, headers=user_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "hooks" in data
    assert len(data["hooks"]) == 10

@pytest.mark.asyncio
async def test_image_prompt_generator(client: AsyncClient, user_headers):
    payload = {"text": "Leather Jacket Poster"}
    resp = await client.post("/api/v1/ai/image-prompt", json=payload, headers=user_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "midjourney" in data
    assert "dalle" in data
    assert "stable_diffusion" in data

@pytest.mark.asyncio
async def test_image_generation(client: AsyncClient, user_headers):
    payload = {"prompt": "Sunset over Indore skyline, high quality digital poster", "provider": "flux"}
    resp = await client.post("/api/v1/ai/generate-image", json=payload, headers=user_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "image_url" in data
    assert len(data["image_url"]) > 0

@pytest.mark.asyncio
async def test_ai_chat_and_memory(client: AsyncClient, user_headers):
    # Send message 1
    payload = {"message": "Hello! Suggest a business idea.", "provider": "gpt"}
    resp = await client.post("/api/v1/chat/", json=payload, headers=user_headers)
    assert resp.status_code == 200
    assert "response" in resp.json()

    # Send message 2 (memory validation fallback)
    payload2 = {"message": "What was my previous question?", "provider": "gpt"}
    resp2 = await client.post("/api/v1/chat/", json=payload2, headers=user_headers)
    assert resp2.status_code == 200
    assert "response" in resp2.json()

    # Get Chat history
    history_resp = await client.get("/api/v1/chat/history", headers=user_headers)
    assert history_resp.status_code == 200
    assert len(history_resp.json()) >= 2

@pytest.mark.asyncio
async def test_saved_results_endpoints(client: AsyncClient, user_headers):
    # Save a result
    payload = {
        "title": "Saved Script",
        "content": "Hook: Stop scrolling. CTA: Click bio.",
        "type": "script"
    }
    create_resp = await client.post("/api/v1/saved/", json=payload, headers=user_headers)
    assert create_resp.status_code == 201
    s_id = create_resp.json()["id"]

    # Get list
    list_resp = await client.get("/api/v1/saved/", headers=user_headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 1
    assert list_resp.json()[0]["title"] == "Saved Script"

    # Delete saved result
    del_resp = await client.delete(f"/api/v1/saved/{s_id}", headers=user_headers)
    assert del_resp.status_code == 200

@pytest.mark.asyncio
async def test_user_history_actions(client: AsyncClient, user_headers):
    # Generate some history
    await client.post("/api/v1/ai/viral-hooks", json={"topic": "History seed"}, headers=user_headers)

    # Get history
    hist_resp = await client.get("/api/v1/history/", headers=user_headers)
    assert hist_resp.status_code == 200
    assert len(hist_resp.json()) >= 1

    # Delete history
    clear_resp = await client.delete("/api/v1/history/", headers=user_headers)
    assert clear_resp.status_code == 200

    # Get history empty check
    hist_empty_resp = await client.get("/api/v1/history/", headers=user_headers)
    assert len(hist_empty_resp.json()) == 0
