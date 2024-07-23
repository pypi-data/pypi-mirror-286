from textual import on
from textual.app import ComposeResult
from textual.widgets import Button, Input, Label, Static

from pgtui import __version__
from pgtui.widgets.menu import Menu, MenuItem
from pgtui.widgets.modal import ModalScreen, ModalTitle


class MessageDialog(ModalScreen[None]):
    DEFAULT_CSS = """
    .dialog_button {
        height: 1;
        min-width: 1;
        border: none;
        border-top: none;
        border-bottom: none;
    }
    """

    def __init__(self, title: str, body: str | None, error: bool = False):
        self.message_title = title
        self.message_body = body
        self.error = error
        super().__init__()

    def compose_modal(self) -> ComposeResult:
        yield ModalTitle(self.message_title, error=self.error)
        if self.message_body:
            yield Static(self.message_body, markup=False)
        yield Button("[ OK ]", variant="default", classes="dialog_button")

    def on_button_pressed(self, message: Button.Pressed):
        self.dismiss()


class ConfirmationDialog(ModalScreen[bool]):
    def __init__(
        self,
        title: str,
        *,
        text: str | None = None,
        confirm_label: str = "Confirm",
        cancel_label: str = "Cancel",
    ):
        self.modal_title = title
        self.modal_text = text
        self.confirm_label = confirm_label
        self.cancel_label = cancel_label
        super().__init__()

    def compose_modal(self) -> ComposeResult:
        yield ModalTitle(self.modal_title)
        if self.modal_text:
            yield Label(self.modal_text)
        with Menu():
            yield MenuItem("confirm", self.confirm_label)
            yield MenuItem("cancel", self.cancel_label)

    @on(Menu.ItemSelected)
    def _on_item_selected(self, message: Menu.ItemSelected):
        message.stop()
        self.dismiss(message.item.code == "confirm")


class ChoiceDialog(ModalScreen[str]):
    def __init__(
        self,
        title: str,
        choices: list[tuple[str, str]],
    ):
        self.modal_title = title
        self.choices = choices
        super().__init__()

    def compose_modal(self) -> ComposeResult:
        yield ModalTitle(self.modal_title)
        with Menu():
            for code, label in self.choices:
                yield MenuItem(code, label)

    @on(Menu.ItemSelected)
    def _on_selected(self, message: Menu.ItemSelected):
        message.stop()
        self.dismiss(message.item.code)


class TextPromptDialog(ModalScreen[str]):
    DEFAULT_CSS = """
    .dialog_text {
        margin-left: 1;
    }

    Input {
        outline: heavy $background;
    }

    Input:focus {
        outline: heavy $accent;
    }
    """

    def __init__(
        self,
        title: str,
        *,
        text: str | None = None,
        initial_value: str | None = None,
        placeholder: str = "",
    ):
        super().__init__()
        self.dialog_title = title
        self.dialog_text = text
        self.initial_value = initial_value
        self.placeholder = placeholder

    def compose_modal(self) -> ComposeResult:
        yield ModalTitle(self.dialog_title)
        if self.dialog_text:
            yield Label(self.dialog_text, classes="dialog_text")
        yield Input(self.initial_value, placeholder=self.placeholder)

    @on(Input.Submitted)
    def on_submitted(self):
        self.dismiss(self.query_one(Input).value)


HELP = """
[bold]Help[/]
  F1 - Show this screen

[bold]Tabs[/]
  Alt+N - New tab
  Alt+W - Close tab
  Alt+<n> - Switch to tab <n>, where n is 1..9
  Alt+Tab - Next tab
  Alt+PageDown - Next tab
  Alt+Shift+Tab - Previous tab
  Alt+PageUp - Previous tab

[bold]Editor[/]
  Alt+D - Select database
  Alt+E - Switch between horizontal and vertical layout
  Alt+O - Open file
  Alt+Q - Quit
  Alt+S - Save
  Ctrl+Enter - Execute query - selected or under cursor
  Ctrl+Space - Autocomplete at cursor
"""


class HelpDialog(ModalScreen[str]):
    def compose_modal(self) -> ComposeResult:
        yield ModalTitle(f"pgtui {__version__}")
        yield Label(HELP)
