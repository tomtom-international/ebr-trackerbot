"""
Slack Bot Memory Storage
"""
import logging
from bot import register_storage
import pendulum
from functools import partial


def delete_for_user(tracks, user, test):
    """
    Delete tracking for user and test
    """
    logging.debug("Delete track for user: " + user + ", test: " + test)
    for track in tracks:
        if track["user"] == user and track["test"] == test:
            tracks.remove(track)


def save(tracks, user, data):
    """
    Create tracking for user and test
    """
    logging.debug("Saving track for user: %s, data: ", user)
    logging.debug(data)
    for index, track in enumerate(tracks):
        if track["user"] == user and track["test"] == data["test"]:
            tracks[index]["expiry"] = data["expiry"]
            tracks[index]["channel_id"] = data["channel_id"]
            tracks[index]["thread_ts"] = data["thread_ts"]
            return
    data["user"] = user
    tracks.append(data)


def load_all_tracked_tests(tracks):
    """
    Load all tracked tests
    """
    return tracks


def load_for_user(tracks, user):
    """
    Load all tracks for user
    """
    return [x for x in tracks if x["user"] == user]


def clean_expired_tracks(tracks):
    """
    Remove expired tracks
    """
    for track in tracks:
        if pendulum.parse(track["expiry"], tz="UTC") < pendulum.now("UTC"):
            tracks.remove(track)


TRACKS = []
register_storage(
    "memory",
    partial(save, TRACKS),
    partial(load_for_user, TRACKS),
    partial(load_all_tracked_tests, TRACKS),
    partial(delete_for_user, TRACKS),
    partial(clean_expired_tracks, TRACKS),
)
logging.info("Memory storage registered")
