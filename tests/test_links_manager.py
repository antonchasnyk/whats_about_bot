from datetime import datetime
import hashlib
from links_manager import add_new_url_to_db
import fakeredis.aioredis
import pytest
import pytz


@pytest.mark.asyncio
async def test_add_new_url_to_db():
    p = fakeredis.aioredis.FakeRedis()
    dt = datetime(year=2021, month=8, day=22, hour=11, minute=24, second=0,
                  microsecond=0, tzinfo=pytz.utc)
    url = 'http://example.com'
    await add_new_url_to_db(url, dt, p)
    key = hashlib.sha1(f'{url}'.encode('utf-8')).hexdigest()
    resp_url, resp_date, resp_visit = await p.hmget(key,
                                                    'url',
                                                    'pub_date',
                                                    'visit')
    assert resp_url.decode('utf-8') == url
    assert resp_date.decode('utf-8') == dt.isoformat()
    assert int(resp_visit) == 0
