"""
Slack Bot List Command
"""

import logging
from bot import register_command
from bot import get_storage


def list_command(text, result, payload, commands):
    """
    Slack Bot List Command
    """
    logging.debug("List command")

    tests = ""
    tracks = get_storage()["load_for_user"](payload["data"]["user"])
    for record in tracks:
        tests += "*" + record["test"] + "* (" + record["expiry"] + ")" + "\n"
    payload["web_client"].chat_postMessage(
        channel=payload["data"]["channel"],
        text="Tracking for following tests:\n" + tests,
        thread_ts=payload["data"]["ts"],
    )


register_command("list", "List tracked tests", "^list$", list_command)
logging.info("List command registered")
