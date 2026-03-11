from configparser import ConfigParser
import appdirs
import datetime
import shutil
from pathlib import Path
import json

_AUTHOR = "szymon-jozef"
_APP_NAME = "zut-calendar"

class Config:
    def __init__(self) -> None:
        self._config_parser = ConfigParser()

        self._config_dir = Path(appdirs.user_config_dir( _APP_NAME, _AUTHOR))
        self._config_dir.mkdir(parents=True, exist_ok=True)
        self._config_file = self._config_dir / "config.ini"

        if not self._config_file.exists():
            self._copy_default_config()

        self._config_parser.read(self._config_file)

        if not self._config_parser.has_section("user"):
            self._config_parser.add_section("user")

        if not self._config_parser.has_section("looks"):
            self._config_parser.add_section("looks")

        self.read_config()


    def read_config(self) -> None:
        self.student_id = self._config_parser.get("user","student_id", fallback=None)
        self.nav = {
                "up" : self._config_parser.get("navigation", "up", fallback="k"),
                "down" : self._config_parser.get("navigation", "down", fallback="j"),
                "left" : self._config_parser.get("navigation", "left", fallback="h"),
                "right" : self._config_parser.get("navigation", "right", fallback="l"),
                "next_week" : self._config_parser.get("navigation", "next_week", fallback="L"),
                "prev_week" : self._config_parser.get("navigation", "prev_week", fallback="H"),
                "refresh" : self._config_parser.get("navigation", "refresh", fallback="f5"),
                "quit" : self._config_parser.get("navigation", "quit", fallback="q")
                }
        self.looks = {
                "scale" : self._config_parser.get("looks", "scale", fallback="4")
                }

    def save_student_id(self, student_id: str | int) -> None:
        self._config_parser.set("user", "student_id", str(student_id))

        with open(self._config_file, "w") as configfile:
            self._config_parser.write(configfile)

    def _copy_default_config(self) -> None:
        try:
            source_path = Path(__file__).parent / "examples" / "config.ini"
            
            if source_path.exists():
                shutil.copy(source_path, self._config_file)
            else:
                self._config_parser.add_section("navigation")
                with open(self._config_file, "w") as f:
                    self._config_parser.write(f)
        except Exception:
            pass


class Cache:
    def __init__(self, fname) -> None:
        self._cache_dir = Path(appdirs.user_cache_dir( _APP_NAME, _AUTHOR))
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._cache_file = self._cache_dir / fname
    
    def get_cache(self) -> dict | list| None:
        if not self._cache_file.exists():
            return None

        with open(self._cache_file, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return None

    def save_cache(self, data: dict | list) -> None:
        with open(self._cache_file, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def exists(self) -> bool:
        return self._cache_file.exists()

class State:
    def __init__(self) -> None:
        self._state_dir = Path(appdirs.user_state_dir(_APP_NAME, _AUTHOR))
        self._state_dir.mkdir(parents=True, exist_ok=True)
        self._state_file = self._state_dir / "state.json"

    def save_last_run(self, last_run: datetime.datetime) -> None:
        state = {
                "last_run": str(last_run)
        }
        with open(self._state_file, "w") as state_file:
            json.dump(state, state_file,  ensure_ascii=False, indent=4)

    def get_last_run(self) -> datetime.datetime | None:
        if not self._state_file.exists():
            return None

        with open(self._state_file, "r") as state_file:
            try:
                return datetime.datetime.fromisoformat(json.load(state_file)["last_run"])
            except (KeyError, ValueError, json.JSONDecodeError):
                return None
