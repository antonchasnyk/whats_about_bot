import asyncio
from datetime import datetime
import logging
import re
from aioredis.client import Redis
import links_manager
import feedparser
from helpers import parse_time


logger = logging.getLogger("crawler")
logging.getLogger("chardet.charsetprober").disabled = True

HREF_RE = re.compile(r'href="(.*?)"')


async def write_one(url: str,
                    pub_date: datetime,
                    redis_pool: Redis,
                    **kwargs) -> None:
    """Write nes article url to redis

    Args:
        url (str): target news article url
        pub_date (str): news article publication date from feed
        redis_pool (Redis): redis connection pool
    """
    await links_manager.add_new_url_to_db(url, pub_date, redis_pool, **kwargs)


async def bulk_write(items: list,
                     redis_pool: Redis,
                     **kwargs) -> None:
    """Write founded urls to redis db

    Args:
        items (list): rss entry list
        redis_pool (Redis): redis client connector
    """
    tasks = []
    for item in items:
        tasks.append(write_one(item[0].id,
                               item[1],
                               redis_pool,
                               **kwargs))
    await asyncio.gather(*tasks)


async def extract_feed_urls(feed: str, **kwargs) -> None:
    loop = asyncio.get_event_loop()
    d = await loop.run_in_executor(None, feedparser.parse, feed)
    items = [(item,
              parse_time(item.published))
             for item in d.entries]
    await bulk_write(items, **kwargs)
