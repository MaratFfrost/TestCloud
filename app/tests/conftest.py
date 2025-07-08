import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app as fastapi_app


@pytest.fixture(scope="function")
async def ac():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    await transport.aclose()
