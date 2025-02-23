import pytest


@pytest.mark.asyncio
async def test_register(client):
    url = "http://127.0.0.1:8000/auth/register"
    async with client.post(url, json={"username": "testuser", "password": "testpass"}) as response:
        assert response.status == 200
        data = await response.json()
        assert data == {"msg": "Пользователь зарегистрирован"}

@pytest.mark.asyncio
async def test_login(client):
    await client.post("/auth/register", json={"username": "testuser", "password": "testpass"})

    response = await client.post("/auth/login", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
