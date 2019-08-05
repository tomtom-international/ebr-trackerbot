#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ebr_trackerbot` package."""

import sys
import os
import re

sys.path.append("ebr_trackerbot")
sys.path.append("ebr_trackerbot/command")

import pytest
from track import track_command
from bot import register_storage, get_storage


def test_track_command():
    register_storage("memory", save_record, "load_for_user", "load_all", "delete_for_user", "clean_expired_tracks")
    assert get_storage()["save"] == save_record
    payload = {}
    payload["web_client"] = type("", (), {})()
    payload["web_client"].chat_postMessage = post_message_commands
    payload["data"] = {}
    payload["data"]["user"] = "test"
    payload["data"]["channel"] = "test"
    payload["data"]["ts"] = "test"
    text = "track test for 10d2h5m10s"
    result = re.match("^track ([^ ]+) for ((?:[0-9]+(?:s|m|h|d))+)$", text, re.IGNORECASE)
    commands = []
    track_command(text, result, payload, commands)


def post_message_commands(channel, text, thread_ts):
    assert re.match(r"^Tracking started for test \*test\* for \*10d2h5m10s\*", text)
    return {"ok": "ok"}


def save_record(user, data):
    return True
