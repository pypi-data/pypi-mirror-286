from functools import cached_property
from pathlib import Path
from typing import Iterable

from textual import on
from textual.app import App
from textual.binding import Binding
from textual.widgets import Footer, Header, TabbedContent, TabPane

from pgtui import __version__
from pgtui.entities import DbContext
from pgtui.messages import ShowException
from pgtui.utils.file import pick_file
from pgtui.widgets.dialog import ConfirmationDialog, ErrorDialog, HelpDialog
from pgtui.widgets.pane import EditorPane
from pgtui.widgets.text_area import SqlTextArea


class PgTuiApp(App[None]):
    TITLE = "pgtui"
    SUB_TITLE = __version__
    CSS_PATH = "app.css"

    BINDINGS = [
        Binding("f1", "help", "Help"),
        Binding("alt+n", "add_pane", "Add pane"),
        Binding("alt+o", "open_file", "Open file"),
        Binding("alt+q", "exit", "Exit pgtui"),
        Binding("alt+1", "switch_tab(0)", show=False),
        Binding("alt+2", "switch_tab(1)", show=False),
        Binding("alt+3", "switch_tab(2)", show=False),
        Binding("alt+4", "switch_tab(3)", show=False),
        Binding("alt+5", "switch_tab(4)", show=False),
        Binding("alt+6", "switch_tab(5)", show=False),
        Binding("alt+7", "switch_tab(6)", show=False),
        Binding("alt+8", "switch_tab(7)", show=False),
        Binding("alt+9", "switch_tab(8)", show=False),
        Binding("alt+0", "switch_tab(9)", show=False),
        Binding("alt+tab", "next_tab", show=False),
        Binding("alt+shift+tab", "prev_tab", show=False),
        Binding("alt+pagedown", "next_tab", show=False),
        Binding("alt+pageup", "prev_tab", show=False),
    ]

    def __init__(self, ctx: DbContext, file_path: Path | None):
        super().__init__()
        self.ctx = ctx
        self.file_path = file_path
        self.animation_level = "none"

    def compose(self):
        yield Header()
        yield TabbedContent(id="editor_tabs")
        yield Footer()

    async def on_mount(self):
        await self.add_pane(self.file_path)

    def on_show_exception(self, message: ShowException):
        self.push_screen(ErrorDialog("Error", str(message.exception)))

    @on(EditorPane.Close)
    def on_pane_close(self, event: EditorPane.Close):
        if event.tab_pane.id is not None:
            self.tc.remove_pane(event.tab_pane.id)

    @on(EditorPane.Dirty)
    def on_pane_dirty(self, event: EditorPane.Dirty):
        label = event.file_path.name if event.file_path else "untitled"
        self.tc.get_tab(event.tab_pane).label = f"{label}*"

    @on(EditorPane.Saved)
    def on_pane_saved(self, event: EditorPane.Saved):
        self.tc.get_tab(event.tab_pane).label = event.file_path.name

    async def add_pane(self, file_path: Path | None = None):
        pane = EditorPane(self.ctx, file_path)
        await self.tc.add_pane(pane)
        self.activate_pane(pane)

    def activate_pane(self, pane: TabPane):
        assert pane.id is not None
        self.tc.active = pane.id

    @on(TabbedContent.TabActivated)
    def _on_tab_activated(self, event: TabbedContent.TabActivated):
        event.pane.query_one(SqlTextArea).focus()

    def action_help(self):
        self.app.push_screen(HelpDialog())

    async def action_add_pane(self):
        await self.add_pane()

    async def action_open_file(self):
        with self.suspend():
            path = await pick_file()
            if path:
                await self.add_pane(path)

    def action_switch_tab(self, no: int):
        panes = self.panes()
        if no < len(panes):
            self.activate_pane(panes[no])

    def action_next_tab(self):
        self._delta_tab(+1)

    def action_prev_tab(self):
        self._delta_tab(-1)

    def _delta_tab(self, delta: int):
        panes = self.panes()
        index = self._active_index(panes)
        if index is not None:
            next_index = (index + delta) % len(panes)
            self.activate_pane(panes[next_index])

    def action_exit(self):
        def on_dismiss(result: bool):
            if result:
                self.app.exit()

        screen = ConfirmationDialog(
            "Quit?",
            confirm_label="Quit",
            cancel_label="Cancel",
        )

        self.app.push_screen(screen, on_dismiss)

    @cached_property
    def tc(self):
        return self.query_one("#editor_tabs", TabbedContent)

    def panes(self):
        return self.tc.query(TabPane)

    def _active_index(self, panes: Iterable[TabPane]) -> int | None:
        if self.tc.active:
            for index, pane in enumerate(panes):
                if pane.id == self.tc.active:
                    return index
