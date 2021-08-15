from asyncio.proactor_events import _ProactorBasePipeTransport
from functools import wraps
import sys
from aioresponses import aioresponses
import pytest
from whats_about import app as quart_app


@pytest.fixture(name="app")
async def _app():
    app = quart_app  # Initialize app
    async with app.test_app() as test_app:
        return test_app


@pytest.fixture
def mock_aioresponse():
    with aioresponses() as m:
        yield m


def silence_event_loop_closed(func):
    """  Work around async Event loop is closed on windows
         https://github.com/aio-libs/aiohttp/issues/4324
    Args:
        func (function): _ProactorBasePipeTransport.__del__

    Returns:
        function: decorated _ProactorBasePipeTransport.__del__
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise
    return wrapper


if sys.platform.lower().startswith('win'):
    # apply a decorator with exception catcher
    _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(
        _ProactorBasePipeTransport.__del__)
