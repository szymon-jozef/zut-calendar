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

    def build_calendar(self, refresh=False) -> Horizontal:
        classes = data.ClassList(api.get_plan(refresh)).list
        today = datetime.today()
        monday = today - timedelta(days=today.weekday())
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        columns = []
        for i in range(7):
            current_day = monday + timedelta(days=i)

            date_str = current_day.strftime("%Y-%m-%d")
            day_name = days[i]

            events_of_day = []

            for event in classes:
                if event.start and event.start.startswith(date_str):
                    events_of_day.append(event)

            columns.append(DayColumn(day_name, events_of_day))

        return Horizontal(*columns, id="main_calendar")
        

    def compose(self) -> ComposeResult:
        yield Header()
        yield self.build_calendar()
        yield Footer()

    async def action_refresh(self):
       await self.query_one("#main_calendar").remove()
       await self.mount(self.build_calendar(True))
        

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
        yield Label(self.data.description)
        yield Label(self.data.worker)

if __name__ == "__main__":
    app = ZutCalendarApp()
    app.run()
