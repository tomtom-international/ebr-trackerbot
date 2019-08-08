"""
Slack Bot ODBC Storage
"""

import pyodbc
import logging
from bot import register_storage, config
import db
from functools import partial


def get_connection():
    '''
    Retrieve odbc connection
    '''
    if config.get("odbc_connection_string") is None:
        raise RuntimeError("Missing odbc_connection_string in configuration")
    return pyodbc.connect(config.get("odbc_connection_string"))


CONN = get_connection()
db.create_table(get_connection(), pyodbc.DatabaseError)
register_storage(
    "odbc",
    partial(db.save, CONN, pyodbc.DatabaseError),
    partial(db.load_for_user, CONN, pyodbc.DatabaseError),
    partial(db.load_all_tracked_tests, CONN, pyodbc.DatabaseError),
    partial(db.delete_for_user, CONN, pyodbc.DatabaseError),
    partial(db.clean_expired_tracks, CONN, pyodbc.DatabaseError),
)
logging.info("ODBC storage registered")
