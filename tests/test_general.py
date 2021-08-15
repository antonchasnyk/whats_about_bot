import pytest


@pytest.mark.asyncio
async def test_index(app):
    async with app.test_client() as client:
        response = await client.get("/")
        assert response.status_code == 200
