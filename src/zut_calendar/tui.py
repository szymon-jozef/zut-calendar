from datetime import datetime, timedelta
from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll, Center, Middle
from textual.screen import ModalScreen
from textual.widgets import Footer, Header, Label, Static
from textual.widget import Widget

from zut_calendar import data, api

class ZutCalendarApp(App):
    CSS_PATH = "./style.tcss"

    BINDINGS = [
            ("q", "quit", "Quit app"),
            ("f5", "refresh", "Refresh")
            #("h", "focus_left","Go left"),
            #("j", "focus_down", "Go down"),
            #("k", "focus_up", "Go up"),
            #("l", "focus_right", "Go right")
            ]

    def compose(self) -> ComposeResult:
        yield Header()

        test_event = data.ClassEntry({"title": "Matematyka", "description": "Sala 101"})
        with Horizontal():
            yield DayColumn("Monday", [test_event, test_event])
            yield DayColumn("Tuesday",[test_event])
            yield DayColumn("Wednesday",[test_event])
            yield DayColumn("Thursday",[test_event])
            yield DayColumn("Friday",[test_event])
            yield DayColumn("Saturday",[test_event])
            yield DayColumn("Sunday",[test_event])
        
        yield Footer()

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
    def __init__(self, info: data.ClassEntry):
        super().__init__()
        self.data: data.ClassEntry = info
        self.can_focus = True

    def compose(self):
        yield Label(self.data.title)
        yield Label(self.data.description)

if __name__ == "__main__":
    app = ZutCalendarApp()
    app.run()
