import asyncio
from urllib.parse import urlparse
import hashlib
import aioredis
from aioredis.client import Redis


async def add_new_url_to_db(request_id: int, url: str, depth: int,
                            redis_pool: Redis):
    """Add to redis db individual url with visit flag

    Args:
        request_id (int): request number to manage different
                          users request in one db
        url (str): target url
        depth (int): current url depths
        redis_pool (Redis): redis_pool obtained by get_redis_pool()
    """
    # obfuscate url params
    upl = urlparse(url)
    clean_url = f'{upl.scheme}://{upl.netloc}{upl.path}'
    # calculate unique hash for each url and request
    key = hashlib.sha1(f'{request_id} {clean_url}'.encode('utf-8')).hexdigest()
    res = await redis_pool.hsetnx(key, 'url', clean_url)
    if res:
        await redis_pool.hset(key, mapping={'url': clean_url,
                                            'depth': depth,
                                            'visit': 0,
                                            })
        await redis_pool.expire(key, 60)


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


if __name__ == '__main__':
    rp = get_redis_pool('redis://localhost/0')
    url = 'https://www.google.com/some_addr/1/page2/index.html?page=20'
    asyncio.run(add_new_url_to_db(100,
                                  url,
                                  1,
                                  rp))
