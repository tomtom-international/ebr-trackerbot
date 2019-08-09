"""
Slack Bot Generic DB Storage
"""

import logging
import pendulum
import sys


def create_table(get_connection):
    """
    Create table if it does not exist
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS tracks "
            + "(id integer PRIMARY KEY, user text NOT NULL, test text NOT NULL, "
            + " expiry timestamp NOT NULL, channel_id text NOT NULL, thread_ts text NOT NULL);"
        )
        conn.commit()
    except:
        logging.error(str(sys.exc_info()[1]))
        conn.close()


def delete_for_user(get_connection, user, test):
    """
    Delete tracking for user and test
    """
    logging.debug("Delete track for user: " + user + ", test: " + test)
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(""" DELETE FROM tracks WHERE user = ? AND test = ?; """, [user, test])
        conn.commit()
    except:
        logging.error(sys.exc_info()[1])
        conn.close()


def save(get_connection, user, data):
    """
    Creates tracking for user and test
    """
    logging.debug("Saving track for user: %s, data: ", user)
    logging.debug(data)
    conn = get_connection()
    try:
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
    except:
        logging.error(sys.exc_info()[1])
        conn.close()


def load_all_tracked_tests(get_connection):
    """
    Load all tracked tests
    """
    result = []
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(""" SELECT user, test, expiry, channel_id, thread_ts FROM tracks; """)
        rows = cursor.fetchall()
        for row in rows:
            data = {
                "user": row[0],
                "test": row[1],
                "expiry": row[2] if isinstance(row[2], str) else pendulum.instance(row[2]).to_iso8601_string(),
                "channel_id": row[3],
                "thread_ts": row[4],
            }
            result.append(data)
        return result
    except:
        logging.error("Error during loading tracks")
        logging.error(sys.exc_info()[1])
        conn.close()


def load_for_user(get_connection, user):
    """
    Load all tracks for user
    """
    result = []
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(""" SELECT user, test, expiry, channel_id, thread_ts FROM tracks WHERE user = ?; """, [user])
        rows = cursor.fetchall()
        for row in rows:
            data = {
                "test": row[1],
                "expiry": row[2] if isinstance(row[2], str) else pendulum.instance(row[2]).to_iso8601_string(),
                "channel_id": row[3],
                "thread_ts": row[4],
            }
            result.append(data)
        return result
    except:
        logging.error("Error during loading track for user")
        logging.error(sys.exc_info()[1])
        conn.close()


def clean_expired_tracks(get_connection):
    """
    Delete expired tracks
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(""" DELETE FROM tracks WHERE expiry < DATETIME('now'); """)
        conn.commit()
    except:
        logging.error("Error during cleaning tracks")
        logging.error(sys.exc_info()[1])
        conn.close()
