from enum import Enum
from datetime import datetime
from . import utils

_ = utils.get_locale_thing()

class ClassType(Enum):
    W = _("lecture")
    A = _("auditorium")
    L = _("laboratory")

class ClassEntry:
    def __init__(self, data):
        short_type = data.get("lesson_form_short")

        self.title = data.get("subject")
        self.description = data.get("description")
        self.start = data.get("start")
        self.end = data.get("end")
        self.worker = data.get("worker")
        self.room = data.get("room")
        self.type = ClassType.__members__.get(short_type) if short_type else None

    def __str__(self) -> str:
        type_str = self.type.value if self.type else _("Unknown type")
        
        t_start = datetime.fromisoformat(self.start).time().strftime("%H:%M")
        t_end = datetime.fromisoformat(self.end).time().strftime("%H:%M")

        lines = [
            f"[b]{_('Title')}:[/b] {self.title}",
            f"[b]{_('Description')}:[/b] {self.description}",
            f"[b]{_('Time')}:[/b] {t_start} - {t_end}",
            f"[b]{_('Worker')}:[/b] {self.worker}",
            f"[b]{_('Room')}:[/b] {self.room}",
            f"[b]{_('Type')}:[/b] {type_str}"
        ]
        return "\n".join(lines)

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
