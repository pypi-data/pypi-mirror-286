from dataclasses import dataclass
from typing import NamedTuple

from psycopg import Column
from psycopg.rows import TupleRow


class Result(NamedTuple):
    """Rows fetched from the database alongside some metadata"""

    rows: list[TupleRow]
    columns: list[Column] | None
    total_rows: int
    fetched_rows: int
    duration: float


@dataclass
class DbInfo:
    """Database info loaded from the server"""

    database: str
    host: str
    host_address: str
    port: str
    schema: str
    user: str


@dataclass
class DbContext:
    """Credentials used to connect to the database"""

    dbname: str | None
    host: str
    password: str | None
    port: str
    username: str
