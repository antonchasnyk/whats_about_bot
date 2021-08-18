from links_manager import get_redis_pool
from quart import Quart
from crawler import bulk_crawl_and_write
import pathlib

app = Quart(__name__)

app_config = {
    'redis_db': 'redis://localhost/0',
}


@app.route('/')
async def info():
    return 'Whats About Config'


@app.route('/walk')
async def start_crawling():
    here = pathlib.Path(__file__).parent
    with open(here.joinpath("urls.txt"), 'r') as infile:
        urls = set(map(str.strip, infile))

    redis_pool = get_redis_pool(app_config['redis_db'])
    await bulk_crawl_and_write(urls=urls, redis_pool=redis_pool)

    return 'Done'

if __name__ == '__main__':
    app.run()
