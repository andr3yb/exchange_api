import pytest
import aiohttp
from app.main import app
from fastapi.testclient import TestClient

@pytest.fixture
async def client():
    """Фикстура для асинхронного тестового клиента с aiohttp."""
    async with aiohttp.ClientSession() as session:
        yield session
