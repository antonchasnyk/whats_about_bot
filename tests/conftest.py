import pytest
from whats_about import app as quart_app


@pytest.fixture(name="app")
async def _app():
    app = quart_app  # Initialize app
    async with app.test_app() as test_app:
        return test_app
