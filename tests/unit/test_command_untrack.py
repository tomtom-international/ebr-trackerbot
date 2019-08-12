#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ebr_trackerbot` package."""

import os
import re
import pytest
from ebr_trackerbot.command.untrack import untrack_command
from ebr_trackerbot.bot import register_storage, get_storage, config


def test_untrack_command():
    config["storage_backend"] = "test"
    register_storage("test", "save", "load_for_user", "load_all", delete, "clean_expired_tracks")
    assert get_storage()["delete_for_user"] == delete
    payload = {}
    payload["web_client"] = type("", (), {})()
    payload["web_client"].chat_postMessage = post_message_commands
    payload["data"] = {}
    payload["data"]["user"] = "test"
    payload["data"]["channel"] = "test"
    payload["data"]["ts"] = "test"
    text = "untrack test"
    result = re.match("^untrack ([^ ]+)$", text, re.IGNORECASE)
    commands = []
    untrack_command(text, result, payload, {}, commands)


def post_message_commands(channel, text, thread_ts):
    assert re.match(r"^Tracking was stopped for test \*test\*", text)
    return {"ok": "ok"}


def delete(user, data):
    return True
