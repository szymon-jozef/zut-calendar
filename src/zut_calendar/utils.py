from zoneinfo import ZoneInfo
from datetime import datetime, timedelta, date
from zut_calendar import io
import os
import gettext


_current_dir = os.path.abspath(os.path.dirname(__file__))
_locale_dir = os.path.join(_current_dir, 'locales')
_t = gettext.translation('zut_calendar', localedir=_locale_dir, fallback=True)
_ = _t.gettext

state = io.State()
config = io.Config()


tz = ZoneInfo("Europe/Warsaw")

def get_now() -> datetime:
    return datetime.now(tz)

def get_today() -> date:
    return datetime.now(tz).date()

def get_dates(week_offset: int) -> tuple[datetime, datetime]:
    now = get_now()
    
    start = now - timedelta(days=now.weekday()) + timedelta(weeks=week_offset)
    start = start.replace(hour=0,minute=0, second=0, microsecond=0)

    end = start + timedelta(days=6)
    end = end.replace(hour=23,minute=59, second=59, microsecond=59)

    return (start, end)
