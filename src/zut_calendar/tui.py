import os
import gettext

from datetime import datetime, timedelta
import asyncio
from textual.app import App, ComposeResult
from textual.validation import Integer
from textual.widgets import Input 
from textual.containers import Horizontal, VerticalScroll, Center, Middle
from textual.screen import ModalScreen
from textual import work
from textual.widgets import Footer, Header, Label, Placeholder, Static
from textual.widget import Widget

from zut_calendar import data, api, io

current_dir = os.path.abspath(os.path.dirname(__file__))
localedir = os.path.join(current_dir, 'locales')
t = gettext.translation('zut_calendar', localedir=localedir, fallback=True)
_ = t.gettext

class ZutCalendarApp(App):
    CSS_PATH = "./style.tcss"

    BINDINGS = [
            ("q", "quit", _("Quit app")),
            ("f5", "refresh", _("Refresh"))
            #("h", "focus_left","Go left"),
            #("j", "focus_down", "Go down"),
            #("k", "focus_up", "Go up"),
            #("l", "focus_right", "Go right")
            ]

    def build_calendar(self, refresh=False) -> Horizontal:
        try:
            classes = data.ClassList(api.get_plan(refresh)).list
        except api.MissingStudentId:
            return Horizontal(Label(_("No student ID found.")), id="main_calendar")
        except ValueError:
            return Horizontal(Label(_("Invalid student ID")), id="main_calendar")

        today = datetime.today()
        monday = today - timedelta(days=today.weekday())
        days = [_("Monday"), _("Tuesday"), _("Wednesday"), _("Thursday"), _("Friday"), _("Saturday"), _("Sunday")]

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

    @work
    async def action_refresh(self):
        try:
            await asyncio.to_thread(api.get_plan, True)
        except (api.MissingStudentId, ValueError) as e:
            config = io.Config()
            if isinstance(e, ValueError):
                self.notify(_("Invalid student ID!"), severity="error")
                config.save_student_id(None)
                
            student_id = await self.app.push_screen_wait(LoginWindow())
            if student_id:
                config.save_student_id(student_id)
                self.action_refresh()
            return

        await self.query_one("#main_calendar").remove()
        await self.mount(self.build_calendar(False)) 
        self.notify(_("Calendar refreshed!"), title=_("Refreshed"), severity="information")

    async def on_mount(self):
        self.action_refresh()

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

class LoginWindow(ModalScreen[str]):
    def compose(self) -> ComposeResult:
        with Center():
            with Middle():
                yield Label(_("Please enter your student ID"))
                yield Input(id="student_id_input", type="integer", max_length=5)

    def on_input_submitted(self, event: Input.Submitted):
        self.dismiss(event.value)

if __name__ == "__main__":
    app = ZutCalendarApp()
    app.run()
