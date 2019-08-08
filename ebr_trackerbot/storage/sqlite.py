"""
Slack Bot SQLite Storage
"""

import sqlite3
from sqlite3 import Error
import db
from functools import partial
from bot import config, register_storage
import logging


def get_filename():
    """
    Returns the filename for the sqlite db
    """
    return config.get("sqlite_filename", "/tmp/data.db")


conn = sqlite3.connect(get_filename())
db.create_table(conn, Error)
register_storage(
    "sqlite",
    partial(db.save, conn, Error),
    partial(db.load_for_user, conn, Error),
    partial(db.load_all_tracked_tests, conn, Error),
    partial(db.delete_for_user, conn, Error),
    partial(db.clean_expired_tracks, conn, Error),
)
logging.info("SQLite storage registered")
