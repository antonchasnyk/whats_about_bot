import asyncio
import logging
from links_manager import get_redis_pool
from quart import Quart
from crawler import extract_feed_urls
import pathlib
import os


logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    filename='processing.log',
)

app = Quart(__name__)
app_config = {}
try:
    app_config['redis_url'] = os.environ['REDIS_URL']
except KeyError:
    app_config['redis_url'] = 'redis://localhost'


@ app.route('/')
async def info():
    return 'Whats About Config'


@ app.route('/walk')
async def start_crawling():
    here = pathlib.Path(__file__).parent
    redis_pool = get_redis_pool(app_config['redis_url'], db=0)
    with open(here.joinpath("feeds.txt"), 'r') as infile:
        urls = set(map(str.strip, infile))

    tasks = []
    for url in urls:
        tasks.append(extract_feed_urls(feed=url, redis_pool=redis_pool))
    await asyncio.gather(*tasks)

    return 'Done'

if __name__ == '__main__':
    app.run()
