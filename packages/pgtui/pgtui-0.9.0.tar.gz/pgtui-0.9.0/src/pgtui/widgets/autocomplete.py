from typing import List, Optional

from pgcli.pgcompleter import Completion  # type: ignore
from rich.segment import Segment
from textual.geometry import Size, clamp
from textual.reactive import reactive
from textual.scroll_view import ScrollView
from textual.strip import Strip


class AutocompleteMenu(ScrollView, can_focus=False):
    DEFAULT_CSS = """
    AutocompleteMenu {
        width: 25;
        height: auto;
        max-height: 20;
        overflow-x: hidden;
        background: $panel;
    }

    AutocompleteMenu:focus {
        background: red;
    }

    .dropdown--highlight {
        background: $accent;
    }
    """

    COMPONENT_CLASSES = {"dropdown--highlight"}

    selected = reactive[Optional[int]](0, always_update=True, init=False)

    def __init__(self, completions: Optional[List[Completion]] = None) -> None:
        super().__init__()
        completions = completions or []
        self.completions = completions
        self.virtual_size = Size(self.size.width, len(completions))

    def update(self, completions: List[Completion]):
        self.completions = completions
        self.virtual_size = Size(self.size.width, len(completions))
        self.selected = 0
        self.refresh()

    @property
    def is_scrollable(self):
        return True

    @property
    def selected_completion(self):
        if self.selected is not None:
            return self.completions[self.selected]

    def render_line(self, y: int) -> Strip:
        _, scroll_y = self.scroll_offset
        y += scroll_y

        if y < len(self.completions):
            highlight_style = self.get_component_rich_style("dropdown--highlight")
            style = highlight_style if y == self.selected else None
            text = self.completions[y].text.ljust(self.size.width)
            return Strip([Segment(text, style)])
        else:
            return Strip.blank(self.size.width)

    def watch_selected(self, _, selected: int | None) -> None:
        _, scroll_y = self.scroll_offset
        _, height = self.container_size

        # Visible row range
        visible_min = scroll_y
        visible_max = scroll_y + height - 1

        # Scroll selected row into view
        if selected is not None:
            if selected > visible_max:
                diff_y = selected - visible_max
                self.scroll_to(None, scroll_y + diff_y, animate=False)

            if selected < visible_min:
                diff_y = visible_min - selected
                self.scroll_to(None, scroll_y - diff_y, animate=False)

    def move_up(self):
        self._move(-1, wrap=True)

    def move_down(self):
        self._move(1, wrap=True)

    def page_up(self):
        self._move(-self.container_size.height, wrap=False)

    def page_down(self):
        self._move(self.container_size.height, wrap=False)

    def _move(self, delta: int, *, wrap: bool = False):
        selected = self.selected or 0
        selected += delta

        if wrap:
            selected = selected % len(self.completions)
        else:
            selected = clamp(selected, 0, len(self.completions) - 1)

        self.selected = selected
