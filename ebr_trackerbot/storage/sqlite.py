"""
Slack Bot SQLite Storage
"""

import sqlite3
import db
from functools import partial
from bot import config, register_storage
import logging


def get_filename():
    """
    Returns the filename for the sqlite db
    """
    return config.get("sqlite_filename", "data.db")


CONN = sqlite3.connect(get_filename())
db.create_table(CONN, sqlite3.Error)
register_storage(
    "sqlite",
    partial(db.save, CONN, sqlite3.Error),
    partial(db.load_for_user, CONN, sqlite3.Error),
    partial(db.load_all_tracked_tests, CONN, sqlite3.Error),
    partial(db.delete_for_user, CONN, sqlite3.Error),
    partial(db.clean_expired_tracks, CONN, sqlite3.Error),
)
logging.info("SQLite storage registered")
