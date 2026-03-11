from datetime import datetime, timedelta
import asyncio
from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll, Vertical
from textual import work
from textual.widget import Widget
from textual.widgets import Footer, Header, Label

from zut_calendar import data, api, io, utils

from .screens import LoginWindow
from .widgets import DateRow, DayColumn, TimeColumn, ClassEvent

_ = utils.get_locale_thing()

class ZutCalendarApp(App):
    CSS_PATH = "./style.tcss"

    def __init__(self, force=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.week_offset = 0
        self.config = io.Config()
        self.force = force

    def compose(self) -> ComposeResult:
        yield Header()
        yield Horizontal(Label(_("Loading...")), id="main_calendar")
        yield Footer()

    @work(exclusive=True)
    async def action_refresh(self, force: bool):
        self.query("#main-calendar-wrapper").remove()
        self.query("#main_calendar").remove() 

        try:
            await self.query_one("#main_calendar").remove()
        except Exception:
            pass
        await self.mount(Horizontal(Label(_("Loading schedule...")), id="main_calendar"))

        try:
            raw_data = await asyncio.to_thread(api.get_plan, force, self.week_offset)
            if raw_data is None:
                raise ValueError("No data returned")
            classes = data.ClassList(raw_data).list
        except (api.MissingStudentId, ValueError):
            await self._handle_login_error()
            return
                
        days = [_("Monday"), _("Tuesday"), _("Wednesday"), _("Thursday"), _("Friday"), _("Saturday"), _("Sunday")]
        header_labels = [Label(" ", id="time-spacer")] 
        for d in days:
            header_labels.append(Label(d, classes="header-day-label"))
        
        header_row = Horizontal(*header_labels, id="calendar-header")
        date_info_row = DateRow(self.week_offset)

        columns = self._build_columns(classes)
        calendar_grid = Horizontal(*columns, id="calendar_grid")
        calendar_grid.styles.height = "auto";


        full_view = Vertical(header_row, date_info_row, VerticalScroll(calendar_grid, id="calendar-scroll-area"), id="main-calendar-wrapper")

        self.query("#main_calendar").remove()
        await self.mount(full_view, before="Footer")

        self.all_events = []
        for col in columns:
            if isinstance(col, DayColumn):
                events_in_col = col.query(ClassEvent)
                self.all_events.extend(list(events_in_col))

        self.all_events.sort(key=lambda x: x.data.start)
        self.focused_event_index = 0

        if force: 
            self.notify(_("Calendar refreshed!"), title=_("Refreshed"), severity="information")

    async def _handle_login_error(self):
        self.notify(_("Invalid student ID or missing data!"), severity="error")
        config = io.Config()
        config.save_student_id(None)
        
        student_id = await self.push_screen(LoginWindow())
        if student_id:
            config.save_student_id(student_id)
            self.action_refresh(True)

    def _build_columns(self, classes) -> list[Widget]:
        today = datetime.today()
        monday = today - timedelta(days=today.weekday()) + timedelta(weeks=self.week_offset)
        
        columns: list[Widget] = [TimeColumn()]
        for i in range(7):
            current_day = monday + timedelta(days=i)
            date_str = current_day.strftime("%Y-%m-%d")
            events_of_day = [e for e in classes if e.start and e.start.startswith(date_str)]
            columns.append(DayColumn(events_of_day)) 
            
        return columns

    def action_prev_week(self):
        self.week_offset -= 1
        self.action_refresh(False)

    def action_next_week(self):
        self.week_offset += 1
        self.action_refresh(False)

    def action_focus_next(self):
        if not hasattr(self, 'all_events') and self.all_events:
            return
        try:
            current_index = self.all_events.index(self.focused)
            self.focused_event_index = (current_index + 1) % len(self.all_events)
        except (ValueError, AttributeError):
            self.focused_event_index = 0

        self.all_events[self.focused_event_index].focus()

    def action_focus_prev(self):
        if not hasattr(self, 'all_events') and self.all_events:
            return
        try:
            current_index = self.all_events.index(self.focused)
            self.focused_event_index = (current_index - 1) % len(self.all_events)
        except (ValueError, AttributeError):
            self.focused_event_index = 0

        self.all_events[self.focused_event_index].focus()

    async def on_mount(self):
        self.bind(self.config.nav_quit, "quit", description=_("Quit app"))
        self.bind(self.config.nav_refresh, "refresh(True)", description=_("Refresh"))
        self.bind(self.config.nav_prev_week, "prev_week", description=_("Week before"))
        self.bind(self.config.nav_next_week, "next_week", description=_("Week next"))
        
        self.bind(self.config.nav_left, "focus_prev", description=_("Go left"))
        self.bind(self.config.nav_up, "focus_prev", description=_("Go up"))
        
        self.bind(self.config.nav_down, "focus_next", description=_("Go down"))
        self.bind(self.config.nav_right, "focus_next", description=_("Go right"))

        self.action_refresh(self.force)
