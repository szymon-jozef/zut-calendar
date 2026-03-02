from configparser import ConfigParser
import appdirs
from pathlib import Path
import json

AUTHOR = "szymon-jozef"
APP_NAME = "zut-calendar"

class Config:
    def __init__(self) -> None:
        self.config_parser = ConfigParser()

        self.config_dir = Path(appdirs.user_config_dir( APP_NAME, AUTHOR))
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "config.ini"

        self.config_parser.read(self.config_file)

        self.student_id = None

    def read_config(self) -> None:
        self.student_id = self.config_parser.get("user","student_id", fallback=None)

    def save(self, student_id: str | int) -> None:
        if not self.config_parser.has_section("user"):
            self.config_parser.add_section("user")

        self.config_parser.set("user", "student_id", str(student_id))

        with open(self.config_file, "w") as configfile:
            self.config_parser.write(configfile)

class Cache:
    def __init__(self) -> None:
        self.cache_dir = Path(appdirs.user_cache_dir( APP_NAME, AUTHOR))
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "cache.json"
    
    def get_cache(self) -> dict | list| None:
        if not self.cache_file.exists():
            print("Cache file doesn't exists...")
            return None

        with open(self.cache_file, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return None

    def save_cache(self, data: dict | list) -> None:
        with open(self.cache_file, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
