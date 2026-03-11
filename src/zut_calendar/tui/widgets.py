from datetime import datetime
from textual.app import ComposeResult
from textual.containers import Vertical, Container, VerticalScroll
from textual.widgets import Label
from textual.widget import Widget

from zut_calendar import data, utils

_ = utils.get_locale_thing()

SCALE = 4
START_HOUR = 8
END_HOUR = 21

class TimeColumn(Widget):
    def compose(self) -> ComposeResult:
        for hour in range(START_HOUR, END_HOUR + 1):
            lbl = Label(f"{hour:02}:00")
            lbl.styles.height = SCALE
            yield lbl

    def on_mount(self):
        self.styles.width = 7

class EventContainer(Container):
    def on_mount(self):
        self.styles.height = (END_HOUR - START_HOUR + 1) * SCALE
        self.styles.position = "relative"
        self.styles.width = "100%"

class DayColumn(Vertical):
    def __init__(self, events: list):
        super().__init__()
        self.events = events

    def on_mount(self):
        self.styles.width = "1fr"
        self.styles.min_width = 25
    
    def compose(self) -> ComposeResult:
        with EventContainer():
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

    def on_mount(self):
        try:
            if self.data.type:
                self.add_class(f"type-{self.data.type.name.lower()}")

            start_dt = datetime.fromisoformat(self.data.start.replace(" ", "T"))
            end_dt = datetime.fromisoformat(self.data.end.replace(" ", "T"))

            start_decimal = start_dt.hour + (start_dt.minute / 60.0)
            end_decimal = end_dt.hour + (end_dt.minute / 60.0)
            
            offset_y = int((start_decimal - START_HOUR) * SCALE)
            height = int((end_decimal - start_decimal) * SCALE)
            
            self.styles.position = "absolute"
            self.styles.offset = (0, offset_y)
            self.styles.height = max(2, height) 
            self.styles.width = "100%"
            
            self.styles.border = ("round", "gray")
            self.styles.background = "dodgerblue 20%"
            
        except Exception:
            pass

    def on_click(self) -> None:
        from .screens import DetailsScreen
        self.app.push_screen(DetailsScreen(self.data))

    def action_show_details(self) -> None:
        from .screens import DetailsScreen
        self.app.push_screen(DetailsScreen(self.data))
