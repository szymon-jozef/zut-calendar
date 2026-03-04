from configparser import ConfigParser
import appdirs
import datetime
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

        self._config_parser.read(self._config_file)

        self.student_id = None
        self.last_run: datetime.date | None = None

    def read_config(self) -> None:
        self.student_id = self._config_parser.get("user","student_id", fallback=None)

        last_run_str = self._config_parser.get("global","last_run", fallback=None)

        if last_run_str:
            try:
                self.last_run = datetime.datetime.fromisoformat(last_run_str).date()
            except ValueError:
                self.last_run = None

    def save_student_id(self, student_id: str | int | None) -> None:
        if not self._config_parser.has_section("user"):
            self._config_parser.add_section("user")

        self._config_parser.set("user", "student_id", str(student_id))

        with open(self._config_file, "w") as configfile:
            self._config_parser.write(configfile)

    def save_last_run(self, last_run: datetime.datetime) -> None:
        if not self._config_parser.has_section("global"):
            self._config_parser.add_section("global")

        self._config_parser.set("global", "last_run", str(last_run))

        with open(self._config_file, "w") as configfile:
            self._config_parser.write(configfile)

class Cache:
    def __init__(self) -> None:
        self._cache_dir = Path(appdirs.user_cache_dir( _APP_NAME, _AUTHOR))
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._cache_file = self._cache_dir / "cache.json"
    
    def get_cache(self) -> dict | list| None:
        if not self._cache_file.exists():
            print("Cache file doesn't exists...")
            return None

        with open(self._cache_file, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return None

    def save_cache(self, data: dict | list) -> None:
        with open(self._cache_file, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
