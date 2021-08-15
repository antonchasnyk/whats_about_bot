import pytest
import crawler
from aiohttp import ClientSession
from aioresponses import aioresponses


@pytest.mark.asyncio
async def test_fetch():
    session = ClientSession()
    with aioresponses() as m:
        m.get('http://123.com', status=200, body=b'test')
        result = await crawler.fetch_html('http://123.com', session=session)
        session.close()
        assert 'test' in result


@pytest.mark.asyncio
async def test_parse():
    session = ClientSession()
    with aioresponses() as m:
        m.get('http://123.com', status=200,
              body="""
              test <a href="https://42.com">...</a> bhla bhla bgal'
              '<broken tag  <a href="https://43.com">...</a>
              """)
        result = await crawler.parse('http://123.com', session=session)
        session.close()
        assert isinstance(result, set)
        assert 'https://42.com' in result
        assert 'https://43.com' in result
