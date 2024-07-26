import asyncio
from functools import wraps

import typer
from fastapi_cli.discover import get_import_string
from fastapi_cli.exceptions import FastAPICLIException
from sqlalchemy import Connection

from ..const import FASTAPI_RTK_TABLES
from ..db import session_manager
from ..globals import g
from ..model import metadata
from .const import logger


async def _init_fastapi_rtk_tables():
    sqlalchemy_url = g.config.get("SQLALCHEMY_DATABASE_URI")
    if not sqlalchemy_url:
        raise Exception("SQLALCHEMY_DATABASE_URI not found in config")

    session_manager.init_db(sqlalchemy_url)
    tables = [
        table for key, table in metadata.tables.items() if key in FASTAPI_RTK_TABLES
    ]

    async with session_manager.connect() as connection:
        if isinstance(connection, Connection):
            metadata.create_all(connection, tables=tables)
        else:
            await connection.run_sync(metadata.create_all, tables=tables)


def ensure_fastapi_rtk_tables_exist(f):
    @wraps(f)
    @_set_migrate_mode
    @_check_existing_app
    def wrapper(*args, **kwargs):
        asyncio.run(_init_fastapi_rtk_tables())
        return f(*args, **kwargs)

    return wrapper


def _check_existing_app(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            get_import_string(path=g.path)
            return f(*args, **kwargs)
        except FastAPICLIException as e:
            logger.error(str(e))
            raise typer.Exit(code=1) from None

    return wrapper


def _set_migrate_mode(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        g.is_migrate = True
        return f(*args, **kwargs)

    return wrapper
