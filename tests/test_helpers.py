from helpers import parse_time
from datetime import datetime, timedelta
import pytz


def test_date_parser():
    '2021-08-22 09:30:00+00:00'
    dt12 = datetime(year=2021, month=8, day=22, hour=12, minute=30, second=0,
                    microsecond=0, tzinfo=pytz.utc)
    dt9 = dt12 - timedelta(hours=3)
    dt19 = dt12 + timedelta(hours=5)
    p1 = parse_time('Sun, 22 Aug 2021 12:30:00 +0300')
    assert p1 == dt9
    p2 = parse_time('Sun, 22 Aug 2021 12:30:00 +0000')
    p3 = parse_time('Sun, 22 Aug 2021 12:30:00 UTC')
    assert p3 == p2 == dt12
    p4 = parse_time('Sun, 22 Aug 2021 12:30:00 UTC+5')
    assert p4 == dt19
