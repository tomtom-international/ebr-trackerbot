"""
Slack Bot SQLite Storage
"""

import sqlite3
from sqlite3 import Error
import logging
from bot import register_storage, config


def get_filename():
    """
    Returns the filename for the sqlite db
    """
    return config.get("sqlite_filename", "data.db")


def create_table():
    """
    Create sqlite table if it does not exist
    """
    try:
        conn = sqlite3.connect(get_filename())
        cursor = conn.cursor()
        cursor.execute(""" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='tracks' """)
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS tracks "
                + "(id integer PRIMARY KEY, user text NOT NULL, test text NOT NULL, "
                + " expiry timestamp NOT NULL, channel_id text NOT NULL, thread_ts text NOT NULL);"
            )
            conn.commit()
    except Error as err:
        logging.error(err)
    finally:
        conn.close()


def delete_for_user(user, test):
    """
    Delete tracking for user and test
    """
    print("Delete track for user: " + user + ", test: " + test)
    try:
        conn = sqlite3.connect(get_filename())
        cursor = conn.cursor()
        cursor.execute(""" DELETE FROM tracks WHERE user = ? AND test = ?; """, [user, test])
        conn.commit()
    except Error as err:
        logging.error(err)
    finally:
        conn.close()


def save(user, data):
    """
    Creates tracking for user and test
    """
    logging.debug("Saving track for user: %s, data: ", user)
    logging.debug(data)
    try:
        conn = sqlite3.connect(get_filename())
        cursor = conn.cursor()
        cursor.execute(
            """ SELECT expiry, channel_id, thread_ts FROM tracks WHERE user = ? AND test = ? """, [user, data["test"]]
        )
        rows = cursor.fetchall()
        if not rows:
            cursor.execute(
                """ INSERT INTO tracks (user, test, expiry, channel_id, thread_ts) VALUES (?, ?, ?, ?, ?); """,
                [user, data["test"], data["expiry"], data["channel_id"], data["thread_ts"]],
            )
        else:
            cursor.execute(
                """ UPDATE tracks SET expiry = ?, channel_id = ?, thread_ts = ? WHERE user = ? AND test = ? """,
                [data["expiry"], data["channel_id"], data["thread_ts"], user, data["test"]],
            )
        conn.commit()
    except Error as err:
        logging.error(err)
    finally:
        conn.close()


def load_all_tracked_tests():
    """
    Load all tracked tests
    """
    result = []
    try:
        conn = sqlite3.connect(get_filename())
        cursor = conn.cursor()
        cursor.execute(""" SELECT user, test, expiry, channel_id, thread_ts FROM tracks; """)
        rows = cursor.fetchall()
        for row in rows:
            data = {"user": row[0], "test": row[1], "expiry": row[2], "channel_id": row[3], "thread_ts": row[4]}
            result.append(data)
        return result
    except Error as err:
        logging.error("Error during loading tracks")
        logging.error(err)
    finally:
        conn.close()


def load_for_user(user):
    """
    Load all tracks for user
    """
    result = []
    try:
        conn = sqlite3.connect(get_filename())
        cursor = conn.cursor()
        cursor.execute(""" SELECT user, test, expiry, channel_id, thread_ts FROM tracks WHERE user = ?; """, [user])
        rows = cursor.fetchall()
        for row in rows:
            data = {"test": row[1], "expiry": row[2], "channel_id": row[3], "thread_ts": row[4]}
            result.append(data)
        return result
    except Error as err:
        logging.error("Error during loading track for user")
        logging.error(err)
    finally:
        conn.close()


def clean_expired_tracks():
    """
    Delete expired tracks
    """
    try:
        conn = sqlite3.connect(get_filename())
        cursor = conn.cursor()
        cursor.execute(""" DELETE FROM tracks WHERE expiry < DATETIME('now'); """)
        conn.commit()
    except Error as err:
        logging.error("Error during cleaning tracks")
        logging.error(err)
    finally:
        conn.close()


create_table()
register_storage("sqlite", save, load_for_user, load_all_tracked_tests, delete_for_user, clean_expired_tracks)
logging.info("SQLite storage registered")
