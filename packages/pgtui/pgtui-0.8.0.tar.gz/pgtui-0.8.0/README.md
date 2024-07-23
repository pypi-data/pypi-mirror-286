pgtui
=====

Terminal user interface for PostgreSQL.

Currently in early development, but getting there.

## Key bindings

* `Tab` - Switch between the editor and results grid
* `Ctrl+C` - Exit

Editor:

* `Ctrl+Enter` - Execute selected query or query under cursor if none selected
* `Ctrl+F` - Format query under cursor
* `Ctrl+S` - Select query under cursor
* `Ctrl+Space` - Show autocomplete

Editor while autocomplete is open:

* `Up/Down/PageUp/Pagedow` - Select row
* `Enter` or `Tab` - Apply autocomplete
* `Esc` - Hide autocomplete

Results grid:

* `S` - Change between cell, line and row selection

## TODO

* see about selecting rows/columns/blocks in the datatable
    * https://github.com/Textualize/textual/discussions/3606
