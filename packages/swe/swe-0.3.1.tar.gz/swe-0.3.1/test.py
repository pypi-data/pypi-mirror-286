import time

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Log


class NoBindingsApp(App[None]):
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("a", "add_text", "Add Log Entry", priority=True),
    ]

    def compose(self) -> ComposeResult:
        yield Footer()
        yield Log()

    def action_add_text(self) -> None:
        self.query_one(Log).write_line(
            f"Captains Log, stardate {time.monotonic():.1f}."
        )


NoBindingsApp().run()
