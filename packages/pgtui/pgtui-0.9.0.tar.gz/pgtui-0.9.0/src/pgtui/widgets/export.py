from pathlib import Path

from textual import work
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button, Input, Label, RadioButton, RadioSet

from pgtui.db import ExportFormat, export_json
from pgtui.entities import DbContext
from pgtui.widgets.dialog import ConfirmationDialog
from pgtui.widgets.modal import ModalScreen, ModalTitle
from pgtui.widgets.status_bar import StatusBar

ID_JSON_DICT = f"export_format_{ExportFormat.JSON_DICT}"
ID_JSON_TUPLE = f"export_format_{ExportFormat.JSON_TUPLE}"
ID_CSV = f"export_format_{ExportFormat.CSV}"


class ExportDialog(ModalScreen[str]):
    DEFAULT_CSS = """
    .dialog_text {
        margin-top: 1;
        margin-left: 1;
    }
    .action_container {
        layout: grid;
        grid-columns: 1fr auto auto;
        grid-size: 3;
        height: auto;
        margin-top: 1;

        Button {
            margin-left: 1;
        }
    }
    """

    def __init__(self, ctx: DbContext, query: str):
        super().__init__()
        self.ctx = ctx
        self.export_query = query
        self.format = ExportFormat.JSON_DICT

    def compose_modal(self) -> ComposeResult:
        yield ModalTitle("Export query")
        yield Label("Export path:", classes="dialog_text")
        yield Input(value="export.json")
        with Container(classes="action_container"):
            with RadioSet():
                yield RadioButton("JSON dicts", value=True, id=ID_JSON_DICT)
                yield RadioButton("JSON tuples", id=ID_JSON_TUPLE)
                yield RadioButton("CSV", id=ID_CSV)
            yield Button("Export", id="ex_export_btn", variant="primary")
            yield Button("Cancel", id="ex_cancel_btn")
        yield StatusBar()

    def show_status(self, message: str):
        self.query_one(StatusBar).set_message(message)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ex_export_btn":
            self.export()

        if event.button.id == "ex_cancel_btn":
            self.dismiss()

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        if not event.pressed.id:
            return

        if event.pressed.id == ID_JSON_TUPLE:
            self.format = ExportFormat.JSON_TUPLE
            self._switch_extension("csv", "json")

        if event.pressed.id == ID_JSON_DICT:
            self.format = ExportFormat.JSON_DICT
            self._switch_extension("csv", "json")

        if event.pressed.id == ID_CSV:
            self.format = ExportFormat.CSV
            self._switch_extension("json", "csv")

    def _switch_extension(self, from_ext: str, to_ext: str):
        input = self.query_one(Input)
        if input.value.endswith(f".{from_ext}"):
            length = len(from_ext) + 1
            input.value = input.value[:-length] + f".{to_ext}"

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.export()

    @work
    async def export(self):
        path = await self._get_path()
        if not path:
            return

        try:
            result = await export_json(self.ctx, self.export_query, path, self.format)
            msg = f"Exported {result.row_count} rows to '{result.path}' in {result.duration}"
            self.dismiss(msg)
        except Exception as ex:
            self.dismiss(f"[red]Export failed: {str(ex)}[/]")

    async def _get_path(self) -> Path | None:
        str_path = self.query_one(Input).value.strip()
        if not str_path.strip():
            self.show_status("[red]No path given[/]")
            return

        path = Path(str_path)
        if path.exists():
            if path.is_dir():
                self.show_status("[red]Given path is an existing directory.[/red]")
                return

            overwrite = await self.app.push_screen_wait(
                ConfirmationDialog(
                    title="Overwrite file?",
                    text=f"{path} already exists. Overwrite?",
                )
            )

            if not overwrite:
                return

        return path
