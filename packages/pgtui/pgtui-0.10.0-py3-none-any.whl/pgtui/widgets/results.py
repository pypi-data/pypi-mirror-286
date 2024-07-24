import re
from itertools import cycle
from typing import Any, Iterable

from psycopg import Column
from psycopg.rows import TupleRow
from textual.app import events
from textual.containers import Container
from textual.widget import Widget
from textual.widgets import DataTable, Label, TabbedContent, TabPane
from textual.widgets.data_table import CursorType

from pgtui.db import Result, ResultSet
from pgtui.utils import random_id
from pgtui.utils.datetime import format_duration
from pgtui.widgets.status_bar import StatusBar


class Results(Widget):
    DEFAULT_CSS = """
    Results:focus-within {
        background: $boost;
    }
    """

    def __init__(self, result_set: ResultSet):
        self.result_set = result_set
        self.pane_ids: list[str] = []
        super().__init__()

    def compose(self):
        results = self.result_set.results

        if not results:
            yield Label("No data")
            return

        elif len(results) == 1:
            [result] = results
            with Container():  # without this scroll is broken
                yield ResultsTable(result.rows, result.columns, classes="single")
                yield StatusBar(self._format_status(result))

        else:
            with TabbedContent():
                for result in results:
                    pane_id = random_id()
                    self.pane_ids.append(pane_id)
                    with TabPane(result.status or "???", id=pane_id):
                        with Container():  # without this scroll is broken
                            yield ResultsTable(result.rows, result.columns)
                            yield StatusBar(self._format_status(result))

    def _format_status(self, result: Result):
        duration = format_duration(result.duration)
        fetched = result.fetched_rows
        total = result.num_rows

        if result.columns:
            if fetched != total:
                return f"Fetched {fetched}/{total} rows in {duration}"
            else:
                return f"Fetched {total} rows in {duration}"
        else:
            return f"Updated {total} rows in {duration}"

    # Switch tabs with alt+n
    def on_key(self, event: events.Key):
        if not self.pane_ids:
            return

        if m := re.match(r"^alt\+([0-9])$", event.key):
            event.stop()
            idx = int(m.group(1)) - 1
            if idx < len(self.pane_ids):
                tc = self.query_one(TabbedContent)
                tc.active = self.pane_ids[idx]
                assert tc.active_pane
                tc.active_pane.query_one(ResultsTable).focus()


class ResultsTable(DataTable[Any]):
    BINDINGS = [
        ("s", "toggle_cursor", "Selection"),
    ]

    def __init__(
        self,
        rows: Iterable[TupleRow] | None = None,
        columns: Iterable[Column] | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ):
        super().__init__(id=id, classes=classes, disabled=disabled)
        self.cursors: Iterable[CursorType] = cycle(["cell", "row", "column", "none"])
        self.cursor_type = next(self.cursors)

        if columns:
            column_names = [c.name for c in columns]
            self.add_columns(*column_names)

        if rows:
            self.add_rows(rows)

    def action_toggle_cursor(self):
        self.cursor_type = next(self.cursors)
