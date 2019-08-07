"""
Slack Bot Track Command
"""

import re
import logging
import requests
from bot import register_command
import pendulum


def show_command(text, result, payload, config, commands):
    """
    Slack Bot Show Command
    """
    logging.debug("Show command")

    target_test = result.group(1)
    duration = result.group(2)
    start = pendulum.now("UTC")
    parts = re.split("([smhdy])", duration)
    number = None
    for part in parts:
        if part in ["s", "m", "h", "d"] and number is not None:
            if part == "s":
                start = start.subtract(seconds=number)
            if part == "m":
                start = start.subtract(minutes=number)
            if part == "h":
                start = start.subtract(hours=number)
            if part == "d":
                start = start.subtract(days=number)
        else:
            try:
                number = int(part)
            except ValueError:
                number = None

    response = requests.get(
        config["api_url"],
        params={
            "test_status": "failed",
            "start": start.to_iso8601_string(),
            "end": pendulum.now("UTC").to_iso8601_string(),
        },
        headers={"accept": "application/json"},
    )

    channel_id = payload["data"]["channel"]
    thread_ts = payload["data"]["ts"]

    if "tests" not in response.json():
        logging.warning("Invalid JSON from api call. Does not contains tests field.")
        payload["web_client"].chat_postMessage(
            channel=channel_id, text="Something went wrong, please report this failure.", thread_ts=thread_ts
        )
        return

    for test in response.json()["tests"]:
        full_name = test["full_name"]
        if full_name == target_test:
            count = str(test["count"])
            payload["web_client"].chat_postMessage(
                channel=channel_id,
                text="Test *{test}* failed {count} times over {duration}".format(
                    test=target_test, count=count, duration=duration
                ),
                thread_ts=thread_ts,
            )
            break
    else:
        payload["web_client"].chat_postMessage(
            channel=channel_id,
            text="Test *{test}* never failed over {duration}".format(test=target_test, duration=duration),
            thread_ts=thread_ts,
        )


register_command(
    "show",
    "Shows the current status of a test over the past time interval. Command syntax: show full_testname over time_interval."
    + "Time interval can contain *s* - seconds, *m* - minutes, *h* - hours, *d* - days"
    + "(eg. 20d5h10m5s)",
    "^show ([^ ]+) over ((?:[0-9]+(?:s|m|h|d))+)$",
    show_command,
)
logging.info("Show command registered")
