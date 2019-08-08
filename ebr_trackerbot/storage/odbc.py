"""
Slack Bot ODBC Storage
"""

import pyodbc
import logging
from bot import register_storage, config
from pyodbc import DatabaseError
import pendulum
import db
from functools import partial


def get_connection():
    if config.get("odbc_connection_string") is None:
        raise RuntimeError("Missing odbc_connection_string in configuration")
    return pyodbc.connect(config.get("odbc_connection_string"))


conn = get_connection()
db.create_table(conn, DatabaseError)
register_storage(
    "odbc",
    partial(db.save, conn, DatabaseError),
    partial(db.load_for_user, conn, DatabaseError),
    partial(db.load_all_tracked_tests, conn, DatabaseError),
    partial(db.delete_for_user, conn, DatabaseError),
    partial(db.clean_expired_tracks, conn, DatabaseError),
)
logging.info("ODBC storage registered")
