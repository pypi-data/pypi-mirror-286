from itertools import chain

from rich.text import Text
from textual.reactive import reactive
from textual.widgets import Static

from pgtui.db import DbInfo


class DbFooter(Static):
    COMPONENT_CLASSES = {"dbfooter--highlight"}

    DEFAULT_CSS = """
    DbFooter {
        background: $accent;
        color: $text;
        dock: bottom;
        height: 1;
    }
    DbFooter > .dbfooter--highlight {
        background: $accent-darken-1;
    }
    """

    db_info: reactive[DbInfo | None] = reactive(None)

    def render(self):
        if self.db_info is None:
            return " Loading database info..."

        highlight_style = self.get_component_rich_style("dbfooter--highlight")

        info = {
            "Database": self.db_info.database,
            "Schema": self.db_info.schema,
            "User": self.db_info.user,
            "Host": self.db_info.host,
            "Port": self.db_info.port,
            "Address": self.db_info.host_address,
        }

        parts = chain.from_iterable(
            [f" {name} ", (f" {value} ", highlight_style)] for name, value in info.items() if value
        )

        return Text.assemble(*parts)
