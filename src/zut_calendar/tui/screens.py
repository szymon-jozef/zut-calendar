from textual.app import  ComposeResult
from textual.widgets import Input 
from textual.containers import  Vertical, Center, Middle
from textual.screen import ModalScreen
from textual.widgets import Footer, Label
from datetime import datetime
from zut_calendar import data, io, utils

_ = utils.get_locale_thing()

class DetailsScreen(ModalScreen):
    _config = io.Config()

    BINDINGS = [
            (_config.nav["quit"], "close_screen", _("Close"))
    ]

    def __init__(self, data: data.ClassEntry):
        super().__init__()
        self.data = data

    def compose(self) -> ComposeResult:
        with Vertical(id="details-dialog"):
            yield Label(str(self.data))
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
