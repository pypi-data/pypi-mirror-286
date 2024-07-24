import json
import logging
import time
from contextlib import asynccontextmanager
from datetime import datetime
from decimal import Decimal
from enum import StrEnum, auto
from pathlib import Path
from typing import Any, List, NamedTuple
from uuid import UUID

import sqlparse
from psycopg import AsyncConnection, AsyncCursor, Column
from psycopg.conninfo import make_conninfo
from psycopg.rows import AsyncRowFactory, Row, TupleRow, dict_row, tuple_row

from pgtui.entities import DbContext, DbInfo
from pgtui.utils.datetime import format_duration

logger = logging.getLogger(__name__)


MAX_FETCH_ROWS = 200
"""
Max rows to fetch at once to avoid loading a very large table into DataTable
accidentally.
TODO: make configurable
"""


class Result(NamedTuple):
    query: str
    rows: list[TupleRow]
    columns: list[Column] | None
    num_rows: int
    fetched_rows: int
    duration: float
    status: str | None


class ResultSet(NamedTuple):
    results: List[Result]
    duration: float


async def fetch_db_info(ctx: DbContext) -> DbInfo:
    query = """
    SELECT current_database() AS database,
           current_user AS user,
           current_schema AS schema;
    """

    async with connect(ctx) as conn:
        cursor = await conn.execute(query)
        row = await cursor.fetchone()
        assert row is not None
        database, user, schema = row

        return DbInfo(
            host=conn.pgconn.host.decode(),
            host_address=conn.pgconn.hostaddr.decode(),
            port=conn.pgconn.port.decode(),
            database=database,
            schema=schema,
            user=user,
        )


async def fetch_databases(ctx: DbContext) -> list[str]:
    query = """
    SELECT datname
    FROM pg_database
    WHERE datallowconn AND NOT datistemplate;
    """

    rows = await select(ctx, query)
    return [r[0] for r in rows]


async def select(ctx: DbContext, query: str) -> list[TupleRow]:
    async with execute(ctx, query) as cursor:
        return await cursor.fetchall()


async def run_queries(ctx: DbContext, queries: str) -> ResultSet:
    results: list[Result] = []
    start = time.monotonic()

    for query in sqlparse.split(queries):
        query_start = time.monotonic()
        async with execute(ctx, query) as cursor:
            result = await _cursor_to_result(cursor, query, query_start)
            results.append(result)

    duration = time.monotonic() - start
    return ResultSet(results, duration)


async def _cursor_to_result(cursor: AsyncCursor[TupleRow], query: str, start: float):
    need_fetch = cursor.description and cursor.rowcount > 0
    rows = await _fetch(cursor) if need_fetch else []
    duration = time.monotonic() - start

    return Result(
        query=query,
        rows=rows,
        columns=cursor.description,
        fetched_rows=len(rows),
        num_rows=cursor.rowcount,
        duration=duration,
        status=cursor.statusmessage,
    )


async def _fetch(cursor: AsyncCursor):
    start = time.monotonic()
    logger.info(f"Fetching {MAX_FETCH_ROWS}/{cursor.rowcount} rows")
    rows = await cursor.fetchmany(MAX_FETCH_ROWS)
    duration = time.monotonic() - start
    logger.info(f"Fetched {len(rows)} rows in {format_duration(duration)}")
    return rows


@asynccontextmanager
async def execute(ctx: DbContext, query: str):
    logger.info(f"Running query: {query}")
    async with connect(ctx) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(query.encode())
            yield cursor


class ExportResult(NamedTuple):
    path: Path
    row_count: int
    duration: float


class ExportFormat(StrEnum):
    JSON_DICT = auto()
    JSON_TUPLE = auto()
    CSV = auto()


async def export_json(
    ctx: DbContext,
    query: str,
    target: Path,
    format: ExportFormat,
) -> ExportResult:
    logger.info(f"Exporting query: {query}")
    start = time.monotonic()

    async with connect(ctx, row_factory=_row_factory(format)) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(query.encode())

            first = True
            with open(target, "w") as f:
                f.write("[")
                async for row in cursor:
                    if not first:
                        f.write(",")
                    first = False
                    f.write(json.dumps(row, cls=DbEncoder))
                f.write("]")

            duration = time.monotonic() - start
            return ExportResult(target, cursor.rowcount, duration)


def _row_factory(format: ExportFormat) -> AsyncRowFactory[Row]:
    # def _row_factory(format: ExportFormat) -> AsyncRowFactory[Row]:
    if format == ExportFormat.JSON_DICT:
        return dict_row

    if format == ExportFormat.JSON_TUPLE:
        return tuple_row

    raise ValueError(f"Invalid format: {format}")


@asynccontextmanager
async def connect(
    ctx: DbContext,
    *,
    row_factory: AsyncRowFactory[Row] | None = None,
):
    conninfo = make_conninfo(
        user=ctx.username,
        password=ctx.password,
        dbname=ctx.dbname,
        host=ctx.host,
        port=ctx.port,
    )

    conn = await AsyncConnection.connect(conninfo, row_factory=row_factory)
    async with conn:
        yield conn


class DbEncoder(json.JSONEncoder):
    def default(self, o: Any):
        if isinstance(o, UUID):
            return o.hex

        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, Decimal):
            return str(o)

        return super().default(o)
