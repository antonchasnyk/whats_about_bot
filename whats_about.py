from quart import Quart
from crawler import bulk_crawl_and_write
import pathlib

app = Quart(__name__)


@app.route('/')
async def info():
    return 'Whats About Config'


@app.route('/walk')
async def start_crawling():
    here = pathlib.Path(__file__).parent
    with open(here.joinpath("urls.txt"), 'r') as infile:
        urls = set(map(str.strip, infile))

    outpath = here.joinpath("foundurls.txt")
    await bulk_crawl_and_write(file=outpath, urls=urls)

    with open(outpath, 'r') as outfile:
        res = list(map(str.strip, outfile))
    return res

if __name__ == '__main__':
    app.run()
