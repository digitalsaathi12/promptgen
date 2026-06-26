import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_ai_chat_json(client: AsyncClient, user_headers):
    payload = {"message": "Kya aap local businesses ko help karte hain?", "provider": "auto"}
    resp = await client.post("/api/v1/ai-chat/", json=payload, headers=user_headers)
    assert resp.status_code == 200
    assert "response" in resp.json()

@pytest.mark.asyncio
async def test_ai_chat_stream(client: AsyncClient, user_headers):
    payload = {"message": "Local business positioning strategies", "provider": "auto"}
    resp = await client.post("/api/v1/ai-chat/stream?language=Hinglish", json=payload, headers=user_headers)
    assert resp.status_code == 200
    assert "text/event-stream" in resp.headers["content-type"]
