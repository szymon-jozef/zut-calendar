import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from urllib.parse import quote
import json
from requests.models import HTTPError

from zut_calendar import config

def _get_dates() -> tuple[str, str]:
    tz = ZoneInfo("Europe/Warsaw")
    now = datetime.now(tz)

    start = now - timedelta(days=now.weekday())
    start = start.replace(hour=0,minute=0, second=0, microsecond=0)

    end = start + timedelta(days=6)
    end = end.replace(hour=23,minute=59, second=59, microsecond=59)

    start_iso = start.isoformat()
    end_iso = end.isoformat()

    start_url = quote(start_iso)
    end_url = quote(end_iso)

    return start_url, end_url

def _get_url() -> str:
    lconfig = config.Config()
    lconfig.read_config()

    student_id = lconfig.student_id

    if student_id is None:
        student_id = input("Please enter your id: ")
        lconfig.save(student_id)

    start, end = _get_dates()

    return f"https://plan.zut.edu.pl/schedule_student.php?number={student_id}&start={start}&end={end}"

def get_plan():
    result = requests.get(_get_url())

    try:
        result.raise_for_status()
    except HTTPError as e:
        print(f"Error while getting http request: {e}")

    plan = json.loads(result.text)

    lcache = config.Cache()
    lcache.save_cache(plan)

    return plan

