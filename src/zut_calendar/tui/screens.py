import os
import gettext

from datetime import datetime, timedelta
import asyncio
from textual.app import App, ComposeResult
from textual.validation import Integer
from textual.widgets import Input 
from textual.containers import Horizontal, Vertical, VerticalScroll, Center, Middle
from textual.screen import ModalScreen
from textual import work
from textual.widgets import Footer, Header, Label, Placeholder, Static
from textual.widget import Widget

from zut_calendar import data, api, io

current_dir = os.path.abspath(os.path.dirname(__file__))
localedir = os.path.join(current_dir, 'locales')
t = gettext.translation('zut_calendar', localedir=localedir, fallback=True)
_ = t.gettext
class DetailsScreen(ModalScreen):
    _config = io.Config()

    BINDINGS = [
            (_config.nav_quit, "close_screen", _("Close"))
    ]

    def __init__(self, class_entry: data.ClassEntry):
        super().__init__()
        self.class_entry = class_entry

    def compose(self) -> ComposeResult:
        with Vertical(id="details-dialog"):
            yield Label(self.class_entry.description)
            # TODO! finish this later
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#details-dialog").border_title = "Information"

    def action_close_screen(self) -> None:
        self.app.pop_screen()

class LoginWindow(ModalScreen[str]):
    def compose(self) -> ComposeResult:
        with Center():
            with Middle():
                yield Label(_("Please enter your student ID"))
                yield Input(id="student_id_input", type="integer", max_length=5)

    def on_input_submitted(self, event: Input.Submitted):
        self.dismiss(event.value)
