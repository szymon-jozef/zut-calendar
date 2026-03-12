from zoneinfo import ZoneInfo
from datetime import datetime, timedelta

def get_locale_thing():
    import os
    import gettext
    current_dir = os.path.abspath(os.path.dirname(__file__))
    localedir = os.path.join(current_dir, 'locales')
    t = gettext.translation('zut_calendar', localedir=localedir, fallback=True)
    _ = t.gettext
    return _

def get_dates(week_offset: int) -> tuple[datetime, datetime]:
    tz = ZoneInfo("Europe/Warsaw")
    now = datetime.now(tz)
    
    start = now - timedelta(days=now.weekday()) + timedelta(weeks=week_offset)
    start = start.replace(hour=0,minute=0, second=0, microsecond=0)

    end = start + timedelta(days=6)
    end = end.replace(hour=23,minute=59, second=59, microsecond=59)

    return (start, end)
