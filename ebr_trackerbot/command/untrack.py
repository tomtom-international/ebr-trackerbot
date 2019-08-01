"""
Slack Bot Untrack Command
"""
import logging
from bot import register_command
from bot import get_storage


def untrack_command(text, result, payload, commands):
    """
    Slack Bot Untrack Command
    """
    logging.debug("Untrack command")

    test = result.group(1)
    get_storage()["delete_for_user"](payload["data"]["user"], test)

    payload["web_client"].chat_postMessage(
        channel=payload["data"]["channel"],
        text="Tracking was stopped for test *" + test + "*",
        thread_ts=payload["data"]["ts"],
    )


register_command(
    "untrack", "Stops test tracking. Command syntax: untrack full_testname", "^untrack ([^ ]+)$", untrack_command
)
logging.info("Untrack command registered")
