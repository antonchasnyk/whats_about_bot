import pytz
from dateutil import parser
from datetime import datetime


def parse_time(pub_date: str) -> datetime:
    """Parse pub_date string to datetime UTC

    Args:
        pub_date (str): publication date from rss tag

    Returns:
        datetime: date and time normalized to UTC
    """
    dt = parser.parse(pub_date)
    utc = pytz.utc
    return dt.astimezone(utc)


# ======================================= Code examples =======================
    # res = await parse(url=url, **kwargs)
    # if not res:
    #     return None
    # tasks = []
    # for p in res:
    #     tasks.append(links_manager.add_new_url_to_db(100, p, 1, redis_pool))
    # await asyncio.gather(*tasks)
    # logger.info("Wrote results for source URL: %s", url)

# from aiohttp import ClientSession
# from aioresponses import aioresponses
# @pytest.mark.asyncio
# async def test_fetch():
#     session = ClientSession()
#     with aioresponses() as m:
#         m.get('http://123.com', status=200, body=b'test')
#         result = await crawler.fetch_html('http://123.com', session=session)
#         session.close()
#         assert 'test' in result


# @pytest.mark.asyncio
# async def test_parse():
#     session = ClientSession()
#     with aioresponses() as m:
#         m.get('http://123.com', status=200,
#               body="""
#               test <a href="https://42.com">...</a> bhla bhla bgal'
#               '<broken tag  <a href="https://43.com">...</a>
#               """)
#         result = await crawler.parse('http://123.com', session=session)
#         session.close()
#         assert isinstance(result, set)
#         assert 'https://42.com' in result
#         assert 'https://43.com' in result
