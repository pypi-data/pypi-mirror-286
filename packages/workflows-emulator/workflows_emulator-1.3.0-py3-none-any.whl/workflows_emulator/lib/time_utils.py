from datetime import datetime
from zoneinfo import ZoneInfo

DATE_FORMAT_ISO_8601 = "%Y-%m-%dT%H:%M:%S.%fZ"


def format(seconds: int | float, tz: str = 'UTC'):
    tzinfo = ZoneInfo(tz)
    dt = datetime.fromtimestamp(seconds, tz=tzinfo)
    return dt.strftime(DATE_FORMAT_ISO_8601)


def parse(value: str) -> float:
    utc_zone = ZoneInfo("UTC") # always assume date in UTC
    d= datetime.strptime(value, DATE_FORMAT_ISO_8601).replace(tzinfo=utc_zone)
    return d.timestamp()
