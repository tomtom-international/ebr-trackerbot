"""
Slack Bot implementation
"""

import asyncio
import os
import re
import sys
import logging
from vault_anyconfig.vault_anyconfig import VaultAnyConfig

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from state import STATE
from checker import check_tests
import slack

config = {}  # pylint: disable=invalid-name


def register_command(command, description, regexp_match, callback):
    """
    Register slack bot command
    """
    if not hasattr(STATE, "bot_command"):
        STATE.bot_command = []
    STATE.bot_command.append(
        {"command": command, "description": description, "regexp_match": regexp_match, "callback": callback}
    )


def register_storage(name, save, load_for_user, load_all_tracked_tests, delete_for_user, clean_expired_tracks):
    """
    Register slack bot storage
    """
    if not hasattr(STATE, "bot_storage"):
        STATE.bot_storage = []
    STATE.bot_storage = [x for x in STATE.bot_storage if x["name"] != name]
    STATE.bot_storage.append(
        {
            "name": name,
            "save": save,
            "load_for_user": load_for_user,
            "load_all_tracked_tests": load_all_tracked_tests,
            "delete_for_user": delete_for_user,
            "clean_expired_tracks": clean_expired_tracks,
        }
    )


def get_storage_name():
    """
    Retrieve storage name
    """
    return config.get("storage_backend", "memory")


def get_storage():
    """
    Returns slack bot storage
    """
    if not hasattr(STATE, "bot_storage"):
        STATE.bot_storage = []
    return list(filter(lambda x: x["name"] == get_storage_name(), STATE.bot_storage))[0]


def slack_message_listener(**payload):
    """
    Listener for slack message event
    """
    data = payload["data"]
    try:
        channel_id = data["channel"]
        thread_ts = data["ts"]
        user = data["user"]
        msg_id = data["client_msg_id"]
    except KeyError:
        logging.debug("Missing one of: channel, ts, user, client_msg_id in slack message")
        return

    if not hasattr(STATE, "last_msgs"):
        STATE.last_msgs = []
    if msg_id in STATE.last_msgs:
        logging.debug("Message already processed")
        return
    if len(STATE.last_msgs) > 10:
        STATE.last_msgs.popleft()
    STATE.last_msgs.append(msg_id)

    logging.info("Incomming message from slack")
    logging.info(data)

    text = ""
    if "text" in data:
        text = re.sub(r"<[^>]+>[ ]+", "", data["text"])

    if not hasattr(STATE, "bot_command"):
        STATE.bot_command = []
    for command in STATE.bot_command:
        result = re.match(command["regexp_match"], text, re.IGNORECASE)
        if result:
            command["callback"](text, result, payload, STATE.bot_command)
            return

    web_client = payload["web_client"]
    web_client.chat_postMessage(
        channel=channel_id,
        text="Hi <@"
        + user
        + ">! \nI don't understand your command. Please type *help* to see all supported commands\n",
        thread_ts=thread_ts,
    )


def configure(config_file, vault_config, vault_creds):
    """
    Loads the configuration of the Slackbot
    Args:
        config_file: filename for the bot configuration file
        vault_config: filename for the vault client configuration file
        vault_creds: filename for the vault credentials file
    """
    global config  # pylint: disable=invalid-name
    config_client = VaultAnyConfig(vault_config)
    config_client.auth_from_file(vault_creds)
    config = config_client.load(config_file)["ebr-trackerbot"]

    log_level = logging.getLevelName(config.get("log_level", "ERROR"))

    logging.basicConfig(
        level=log_level, format="[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    if "api_url" not in config:
        raise RuntimeError("Missing api url in configuration.")
    if "slack_token" not in config:
        raise RuntimeError("Missing Slack Token in configuration.")

    default_slack_message_template = "Test *{{test}}* failed *{{count}}* in the last {{period}}\n"
    config.setdefault("slack_message_template", default_slack_message_template)

    config.setdefault("check_tests_delay", 86400)  # in seconds, 86400 = 1 day


def main(config_file, vault_config, vault_creds):
    """
    Initialize slack bot
    Args:
        config_file: filename for the bot configuration file
        vault_config: filename for the vault client configuration file
        vault_creds: filename for the vault credentials file
    """
    configure(config_file, vault_config, vault_creds)

    import storage  # pylint: disable-msg=unused-import
    import command  # pylint: disable-msg=unused-import

    logging.info("Backend: %s", get_storage_name())
    loop = asyncio.get_event_loop()
    slack_client = slack.WebClient(token=config["slack_token"], run_async=True)
    loop.call_later(
        config["check_tests_delay"],
        check_tests,
        loop,
        config["check_tests_delay"],
        get_storage(),
        slack_client,
        config["api_url"],
        config["slack_message_template"],
    )
    rtm_client = slack.RTMClient(token=config["slack_token"])
    rtm_client.on(event="message", callback=slack_message_listener)
    rtm_client.start()
