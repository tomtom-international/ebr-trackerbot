"""
Slack Bot SQLite Storage
"""

import sqlite3
import logging
import tempfile
from functools import partial
from ebr_trackerbot.storage import db
from ebr_trackerbot.bot import config, register_storage


def get_connection(config):
    if get_connection.link is None:
        get_connection.link = sqlite3.connect(config.get("sqlite_filename", tempfile.gettempdir() + "/data.db"))
        db.create_table(lambda: get_connection.link)
    try:
        cursor = get_connection.link.cursor()
        cursor.close()
    except:
        get_connection.link = sqlite3.connect(config.get("sqlite_filename", tempfile.gettempdir() + "/data.db"))
        db.create_table(lambda: get_connection.link)

    return get_connection.link


get_connection.link = None

register_storage(
    "sqlite",
    partial(db.save, partial(get_connection, config)),
    partial(db.load_for_user, partial(get_connection, config)),
    partial(db.load_all_tracked_tests, partial(get_connection, config)),
    partial(db.delete_for_user, partial(get_connection, config)),
    partial(db.clean_expired_tracks, partial(get_connection, config)),
)
logging.info("SQLite storage registered")
