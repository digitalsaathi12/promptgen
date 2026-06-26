import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_list_users_admin(client: AsyncClient, admin_headers):
    resp = await client.get("/api/v1/admin/users", headers=admin_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

@pytest.mark.asyncio
async def test_list_users_user_unauthorized(client: AsyncClient, user_headers):
    resp = await client.get("/api/v1/admin/users", headers=user_headers)
    assert resp.status_code == 403

@pytest.mark.asyncio
async def test_admin_analytics(client: AsyncClient, admin_headers):
    resp = await client.get("/api/v1/admin/analytics", headers=admin_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "total_users" in data
    assert "total_prompts" in data
    assert "ai_usage_stats" in data
    assert "subscriptions_count" in data
    assert "recent_activities" in data
