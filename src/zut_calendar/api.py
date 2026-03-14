import requests
from textual import log
from datetime import timedelta
from urllib.parse import quote
from requests.models import HTTPError

from zut_calendar import io
from zut_calendar.utils import _, get_dates, config, state, get_now

class MissingStudentId(Exception):
    pass

def _get_dates(week_offset=0) -> tuple[str, str]:
    start, end = get_dates(week_offset)
    
    start_iso = start.isoformat()
    end_iso = end.isoformat()

    start_url = quote(start_iso)
    end_url = quote(end_iso)

    return start_url, end_url

def _get_url(week_offset=0) -> str:
    config.read_config()

    student_id = config.student_id

    if student_id is None:
        raise MissingStudentId(_("No student id found"))

    student_id_str = str(student_id).strip()

    if not student_id_str or student_id_str == "None" or len(student_id_str) < 4:
        raise ValueError(_("Invalid student ID format"))

    start, end = _get_dates(week_offset)

    return f"https://plan.zut.edu.pl/schedule_student.php?number={student_id}&start={start}&end={end}"

def get_plan(force_refresh=False, week_offset=0):
    now = get_now()
    start = now - timedelta(days=now.weekday()) + timedelta(weeks=week_offset)
    cache_name = start.strftime("%G-W%V-%u.json")
    cache = io.Cache(cache_name)

    last_run = state.get_last_run()
    if not force_refresh:

        if last_run is not None and cache.exists():
            time_diff = now - last_run
            if time_diff < timedelta(hours=2):
                log.info(_("Last refresh was less than 2h ago ({:.0f} min), reading cache...").format(time_diff.total_seconds() / 60))
                return cache.get_cache()

    result = requests.get(_get_url(week_offset))

    try:
        result.raise_for_status()
    except HTTPError as e:
        log.error(_("Error while getting http request: {}").format(e))
        raise ValueError("HTTP Error")

    plan = result.json()
    cache.save_cache(plan)
    state.save_last_run(now)

    return plan
