from enum import Enum
from . import utils

_ = utils.get_locale_thing()

class ClassType(Enum):
    W = _("lecture")
    A = _("auditorium")
    L = _("laboratory")

class ClassEntry:
    def __init__(self, data):
        short_type = data.get("lesson_form_short")

        self.title = data.get("title")
        self.description = data.get("description")
        self.start = data.get("start")
        self.end = data.get("end")
        self.worker = data.get("worker")
        self.type = ClassType.__members__.get(short_type) if short_type else None

    def __str__(self) -> str:
        type_str = self.type.value if self.type else "Unknown type"

        return f"""
        Title = {self.title}
        Description = {self.description}
        Start = {self.start}
        End = {self.end}
        Worker = {self.worker}
        Type = {type_str}
        """

class ClassList:
    def __init__(self, json) -> None:
        self.list = []
        for item in json[1:]:
            if isinstance(item, dict):
                self.list.append(ClassEntry(item))

    def __str__(self) -> str:
        string = ""
        for element in self.list:
            string += str(element)

        return string
