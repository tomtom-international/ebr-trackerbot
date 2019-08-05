"""
Slack Bot Memory Storage
"""
import logging
from bot import register_storage
import pendulum

TRACKS = []


def delete_for_user(user, test):
    """
    Delete tracking for user and test
    """
    global TRACKS
    logging.debug("Delete track for user: " + user + ", test: " + test)
    TRACKS = [x for x in TRACKS if x["user"] != user and x["test"] != test]


def save(user, data):
    """
    Create tracking for user and test
    """
    global TRACKS
    logging.debug("Saving track for user: %s, data: ", user)
    logging.debug(data)
    for index, track in enumerate(TRACKS):
        if track["user"] == user and track["test"] == data["test"]:
            TRACKS[index]["expiry"] = data["expiry"]
            TRACKS[index]["channel_id"] = data["channel_id"]
            TRACKS[index]["thread_ts"] = data["thread_ts"]
            return
    data["user"] = user
    TRACKS.append(data)


def load_all_tracked_tests():
    """
    Load all tracked tests
    """
    global TRACKS
    return TRACKS


def load_for_user(user):
    """
    Load all tracks for user
    """
    global TRACKS
    return [x for x in TRACKS if x["user"] == user]


def clean_expired_tracks():
    """
    Remove expired tracks
    """
    global TRACKS
    TRACKS = [x for x in TRACKS if pendulum.parse(x["expiry"]) > pendulum.now("UTC")]


register_storage("memory", save, load_for_user, load_all_tracked_tests, delete_for_user, clean_expired_tracks)
logging.info("Memory storage registered")
