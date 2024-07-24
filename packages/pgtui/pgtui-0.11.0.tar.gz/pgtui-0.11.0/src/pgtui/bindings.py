from typing import NamedTuple


class Bindings(NamedTuple):
    select_database = "alt+d"
    switch_layout = "alt+e"
    save = "alt+s"
    close = "alt+w"
    execute_query = "ctrl+enter,ctrl+full_stop"
    autocomplete = "ctrl+space"
    format_query = "alt+f"
    format_all = "alt+shift+f"
    select_query = "alt+e"
    copy_query = "alt+c"
    close_autocomplete = "escape"


def load_bindings(): ...
