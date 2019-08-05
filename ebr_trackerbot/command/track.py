"""
Slack Bot Track Command
"""

import re
import logging
from bot import register_command
from bot import get_storage
import pendulum


def track_command(text, result, payload, commands):
    """
    Slack Bot Track Command
    """
    logging.debug("Track command")

    test = result.group(1)
    duration = result.group(2)
    expiry = pendulum.now("UTC")
    parts = re.split("([smhdy])", duration)
    number = None
    for part in parts:
        if part in ["s", "m", "h", "d"] and number is not None:
            if part == "s":
                expiry = expiry.add(seconds=number)
            if part == "m":
                expiry = expiry.add(minutes=number)
            if part == "h":
                expiry = expiry.add(hours=number)
            if part == "d":
                expiry = expiry.add(days=number)
        else:
            try:
                number = int(part)
            except ValueError:
                number = None

    channel_id = payload["data"]["channel"]
    thread_ts = payload["data"]["ts"]
    get_storage()["save"](
        payload["data"]["user"],
        {"test": test, "expiry": expiry.to_iso8601_string(), "channel_id": channel_id, "thread_ts": thread_ts},
    )

    payload["web_client"].chat_postMessage(
        channel=channel_id,
        text="Tracking started for test *" + test + "* for *" + duration + "* (" + expiry.to_iso8601_string() + ")",
        thread_ts=thread_ts,
    )


register_command(
    "track",
    "Starts test tracking. Command syntax: track full_testname for time_interval."
    + "Time interval can contain *s* - seconds, *m* - minutes, *h* - hours, *d* - days"
    + "(eg. 20d5h10m5s)",
    "^track ([^ ]+) for ((?:[0-9]+(?:s|m|h|d))+)$",
    track_command,
)
logging.info("Track command registered")
