"""
Checks for failing test from api
"""

import logging
import asyncio
import requests
import pendulum


def check_tests(
    loop, check_tests_delay, storage, slack_client, api_url, br_url
):  # pylint: disable-msg=too-many-arguments
    """
    Check tests and send slack message to user when some tracked tests failed
    """
    logging.info("Check tests results")
    loop.call_later(check_tests_delay, check_tests, loop, check_tests_delay, storage, slack_client, api_url, br_url)
    end = pendulum.now("UTC")
    start = pendulum.now("UTC").substract(hours=24)
    response = requests.get(
        api_url,
        params={"test_status": "failed", "start": start.to_iso8601_string(), "end": end.to_iso8601_string()},
        headers={"accept": "application/json"},
    )
    storage["clean_expired_tracks"]()
    tracks = storage["load_all_tracked_tests"]()

    if "tests" not in response.json():
        logging.warning("Invalid JSON from api call. Does not contains tests field.")
        return

    for test in response.json()["tests"]:
        full_name = test["full_name"]
        count = test["count"]
        for track in tracks:
            if full_name != track["test"]:
                continue
            asyncio.wait(send_track(track, count, check_tests_delay, slack_client, br_url))


def send_track(track, count, check_tests_delay, client, br_url):
    """
    Send slack message
    """
    logging.info("Sending message to client. USER: %s, TEST: %s FAILED", track["user"], track["test"])
    link = ""
    if br_url is not None:
        link = br_url + track["test"]
    return client.chat_postMessage(
        channel=track["channel_id"],
        text="Test *"
        + track["test"]
        + "* failed *"
        + str(count)
        + "x* in the last "
        + pendulum.period(
            pendulum.now("UTC").subtract(seconds=check_tests_delay), pendulum.now("UTC")
        ).in_words()
        + "\n"
        + link,
        thread_ts=track["thread_ts"],
    )
