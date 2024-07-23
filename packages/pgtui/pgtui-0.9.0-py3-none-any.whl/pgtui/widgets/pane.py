import logging
from asyncio import Lock
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from psycopg import Error
from psycopg.rows import TupleRow
from rich.text import Text
from textual import on, work
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import TabPane, TextArea

from pgtui.completer import QueryCompleter
from pgtui.db import ResultSet, fetch_databases, fetch_db_info, run_queries
from pgtui.entities import DbContext
from pgtui.messages import RunQuery, ShowException
from pgtui.utils import random_id
from pgtui.widgets.containers import SwitchingLayout
from pgtui.widgets.dialog import ChoiceDialog, ConfirmationDialog, MessageDialog, TextPromptDialog
from pgtui.widgets.editor import SqlEditor
from pgtui.widgets.footer import DbFooter
from pgtui.widgets.results import Results
from pgtui.widgets.text_area import SqlTextArea

logger = logging.getLogger(__name__)


class EditorPane(TabPane):
    BINDINGS = [
        Binding("alt+d", "select_database", "Select database"),
        Binding("alt+e", "switch_layout", "Switch layout"),
        Binding("alt+s", "save", "Save"),
    ]

    DEFAULT_CSS = """
    Container.results {
        &:focus-within {
            background: $boost;
        }
    }
    """

    @dataclass
    class Saved(TabPane.TabPaneMessage):
        file_path: Path

    @dataclass
    class Dirty(TabPane.TabPaneMessage):
        file_path: Path

    def __init__(self, ctx: DbContext, file_path: Path | None):
        self.ctx = ctx
        self.file_path = file_path
        self.exec_lock = Lock()
        self.dirty = False

        title = file_path.name if file_path else Text("untitled", "dim")
        completer = self._make_completer(ctx)

        super().__init__(
            title,
            SwitchingLayout(
                SqlEditor(completer, self.file_path),
                Container(classes="results"),
            ),
            DbFooter(),
            id=random_id(),
        )

    def _make_completer(self, ctx: DbContext):
        return QueryCompleter(
            database=ctx.dbname,
            user=ctx.username,
            password=ctx.password,
            host=ctx.host,
            port=ctx.port,
        )

    def on_mount(self):
        self.load_db_info()

    @work
    async def load_db_info(self):
        db_info = await fetch_db_info(self.ctx)
        self.query_one(DbFooter).db_info = db_info

    @work
    async def run_query(self, query: str):
        if self.exec_lock.locked():
            return

        try:
            async with self.exec_lock:
                result_set = await run_queries(self.ctx, query)
                await self.show_results(result_set)
        except Error as ex:
            logger.info(f"Query failed: {ex}")
            self.post_message(ShowException(ex))

    async def on_run_query(self, message: RunQuery):
        self.last_query = None
        self.run_query(message.query)

    async def show_results(self, result_set: ResultSet):
        container = self.query_one(".results", Container)
        async with container.batch():
            await container.remove_children()
            await container.mount(Results(result_set))

    @on(TextArea.Changed)
    def on_changed(self, _):
        if self.file_path and not self.dirty:
            self.dirty = True
            self.post_message(self.Dirty(self, self.file_path))

    def action_switch_layout(self):
        self.query_one(SwitchingLayout).switch()

    @work
    async def action_select_database(self):
        databases = await fetch_databases(self.ctx)
        choices = [(db, db) for db in databases]
        dialog = ChoiceDialog("Select database", choices)
        dbname = await self.app.push_screen_wait(dialog)
        if dbname:
            self.ctx.dbname = dbname
            self.query_one(DbFooter).db_info = await fetch_db_info(self.ctx)
            self.query_one(SqlEditor).completer = self._make_completer(self.ctx)

    @work
    async def action_save(self):
        if not self.file_path:
            self.file_path = await self._get_new_file_path()

        if not self.file_path:
            return

        # TODO: handle errors
        with open(self.file_path, "w") as f:
            contents = self.query_one(SqlTextArea).text
            f.write(contents)

        self.dirty = False
        self.post_message(self.Saved(self, self.file_path))

    async def _get_new_file_path(self) -> Path | None:
        path = await self._prompt_save_path()
        if not path:
            return

        if path.is_dir():
            dialog = MessageDialog("Invalid path", "Given path is a directory", error=True)
            self.app.push_screen(dialog)
            return

        if path.exists() and not await self._confirm_overwrite(path):
            return

        return path

    async def _prompt_save_path(self) -> Path | None:
        dialog = TextPromptDialog("File path", initial_value="foo.sql")
        path = await self.app.push_screen_wait(dialog)
        return Path(path) if path.strip() else None

    async def _confirm_overwrite(self, path: Path) -> bool:
        dialog = ConfirmationDialog("Overwrite?", text=f"File '{path}' exists, overwrite?")
        return await self.app.push_screen_wait(dialog)


NULL = Text("<null>", "dim")


def mark_nulls(rows: Iterable[TupleRow]) -> Iterable[TupleRow]:
    """Replaces nulls in db data with a styled <null> marker."""
    return (tuple(cell if cell is not None else NULL for cell in row) for row in rows)
