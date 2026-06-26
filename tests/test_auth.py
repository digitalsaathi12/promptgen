import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient):
    # 1. Register
    payload = {
        "name": "Alex Smith",
        "email": "alex@example.com",
        "password": "securepassword123",
        "language_pref": "en"
    }
    resp = await client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 201
    assert resp.json()["email"] == "alex@example.com"
    assert "id" in resp.json()

    # Duplicate Check
    resp_dup = await client.post("/api/v1/auth/register", json=payload)
    assert resp_dup.status_code == 400

    # 2. Login
    login_payload = {
        "email": "alex@example.com",
        "password": "securepassword123"
    }
    resp_login = await client.post("/api/v1/auth/login", json=login_payload)
    assert resp_login.status_code == 200
    data = resp_login.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_get_and_update_me(client: AsyncClient, user_headers):
    # 1. Get Me
    resp = await client.get("/api/v1/auth/me", headers=user_headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == "testuser@example.com"

    # 2. Update Me
    payload = {"name": "New Name", "language_pref": "hinglish"}
    resp_up = await client.put("/api/v1/auth/me", json=payload, headers=user_headers)
    assert resp_up.status_code == 200
    assert resp_up.json()["name"] == "New Name"
    assert resp_up.json()["language_pref"] == "hinglish"
