import os
import gettext

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Label
from textual.widget import Widget

from zut_calendar import data

current_dir = os.path.abspath(os.path.dirname(__file__))
localedir = os.path.join(current_dir, 'locales')
t = gettext.translation('zut_calendar', localedir=localedir, fallback=True)
_ = t.gettext


class DayColumn(VerticalScroll):
    def __init__(self, day_name, events: list):
        super().__init__()
        self.day_name = day_name
        self.events = events
    
    def compose(self) -> ComposeResult:
        yield Label(self.day_name)

        for event in self.events:
            yield ClassEvent(event)

class ClassEvent(Widget):
    BINDINGS = [
            ("enter", "show_details", _("Show details"))
    ]

    def __init__(self, info: data.ClassEntry):
        super().__init__()
        self.data: data.ClassEntry = info
        self.can_focus = True

    def compose(self):
        yield Label(self.data.description)
        yield Label(self.data.worker)
        type_str = self.data.type.value if self.data.type else "Unknown"
        yield Label(type_str)

    def on_click(self) -> None:
        from .screens import DetailsScreen
        self.app.push_screen(DetailsScreen(self.data))

    def action_show_details(self) -> None:
        from .screens import DetailsScreen
        self.app.push_screen(DetailsScreen(self.data))

