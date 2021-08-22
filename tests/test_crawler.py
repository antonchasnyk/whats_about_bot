from datetime import datetime
import pytz
import pytest
import crawler
from unittest.mock import Mock, patch


def parse_mock(feed: str):
    data = Mock()
    items = [Mock() for i in range(10)]
    for i, item in enumerate(items):
        item.published = 'Sun, 22 Aug 2021 14:24:00 +0300'
        item.id = f'https://example.com/{i}'
    data.entries = items
    return data


@pytest.mark.asyncio
@patch('feedparser.parse', parse_mock)
@patch('crawler.bulk_write')
async def test_extract_feed_urls(mock_bulk_write):
    await crawler.extract_feed_urls('https://www.pravda.com.ua/rus/rss/')
    assert mock_bulk_write.called
    items = mock_bulk_write.call_args[0][0]
    dt = datetime(year=2021, month=8, day=22, hour=11, minute=24, second=0,
                  microsecond=0, tzinfo=pytz.utc)
    for i, item in enumerate(items):
        assert item[0].id == f'https://example.com/{i}'
        assert item[1] == dt


@pytest.mark.asyncio
@patch('crawler.write_one')
async def test_bulk_write(mock_write_one):
    # prepareing test data
    articles = [Mock() for i in range(5)]
    dt = datetime(year=2021, month=8, day=22, hour=11, minute=24, second=0,
                  microsecond=0, tzinfo=pytz.utc)
    for i, a in enumerate(articles):
        a.id = f'https://example.com/{i}'
    items = [(item, dt) for item in articles]
    await crawler.bulk_write(items, None)
    assert mock_write_one.called
    arg_url = mock_write_one.call_args[0][0]
    arg_dt = mock_write_one.call_args[0][1]
    assert arg_dt == dt
    assert arg_url == 'https://example.com/4'


@pytest.mark.asyncio
@patch('links_manager.add_new_url_to_db')
async def test_write_one(mock_add_new_url_to_db):
    dt = datetime(year=2021, month=8, day=22, hour=11, minute=24, second=0,
                  microsecond=0, tzinfo=pytz.utc)
    await crawler.write_one('http://example/one.xml', dt, None)
    assert mock_add_new_url_to_db.called
    assert mock_add_new_url_to_db.call_args[0][0] == 'http://example/one.xml'
    assert mock_add_new_url_to_db.call_args[0][1] == dt
