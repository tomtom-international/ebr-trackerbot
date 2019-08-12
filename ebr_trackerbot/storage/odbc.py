"""
Slack Bot ODBC Storage
"""

import pyodbc
import logging
from ebr_trackerbot.bot import register_storage, config
from ebr_trackerbot.storage import db
from functools import partial


def create_connection(config):
    if config.get("odbc_connection_string") is None:
        raise RuntimeError("Missing odbc_connection_string in configuration")
    link = pyodbc.connect(config.get("odbc_connection_string"))
    db.create_table(lambda: link)
    return link


def get_connection(config):
    """
    Retrieve odbc connection
    """
    if get_connection.link is None:
        get_connection.link = create_connection(config)
    try:
        cursor = get_connection.link.cursor()
        cursor.close()
    except:
        get_connection.link = create_connection(config)
    return get_connection.link


get_connection.link = None

register_storage(
    "odbc",
    partial(db.save, partial(get_connection, config)),
    partial(db.load_for_user, partial(get_connection, config)),
    partial(db.load_all_tracked_tests, partial(get_connection, config)),
    partial(db.delete_for_user, partial(get_connection, config)),
    partial(db.clean_expired_tracks, partial(get_connection, config)),
)
logging.info("ODBC storage registered")
