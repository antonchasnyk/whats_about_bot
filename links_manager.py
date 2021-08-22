import hashlib
import aioredis
from aioredis.client import Redis
from datetime import datetime
import pytz


async def add_new_url_to_db(url: str, pub_date: datetime,
                            redis_pool: Redis):
    """Add to redis db individual url with visit flag

    Args:
        url (str): target url
        depth (int): current url depths
        redis_pool (Redis): redis_pool obtained by get_redis_pool()
    """
    # calculate unique hash for each url and request
    key = hashlib.sha1(f'{url}'.encode('utf-8')).hexdigest()
    res = await redis_pool.hsetnx(key, 'url', url)
    if res:
        date_str = pub_date.astimezone(
            pytz.utc).replace(microsecond=0).isoformat()
        await redis_pool.hset(key, mapping={'url': url,
                                            'pub_date': date_str,
                                            'visit': 0,
                                            })
        await redis_pool.expire(key, 60)  # TODO remove in prodaction


def get_redis_pool(db_url: str) -> Redis:
    """Return Redis pool by connection string

    Args:
        db_url (str): redis db address string

    Returns:
        Redis: redis_pool for use store function
    """
    return aioredis.from_url(
        db_url, encoding="utf-8", decode_responses=True
    )
