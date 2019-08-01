#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ebr_trackerbot` package."""

import sys
import os

sys.path.append("ebr_trackerbot")
sys.path.append("ebr_trackerbot/command")

import pytest
from list import list_command
from bot import register_storage


def test_list_command():
    register_storage("memory", "save", load_for_user, "load_all", "delete_for_user", "clean_expired_tracks")
    payload = {}
    payload["web_client"] = type("", (), {})()
    payload["web_client"].chat_postMessage = post_message_commands
    payload["data"] = {}
    payload["data"]["user"] = "test"
    payload["data"]["channel"] = "test"
    payload["data"]["ts"] = "test"
    text = "list"
    result = "list"
    commands = []
    list_command(text, result, payload, commands)


def post_message_commands(channel, text, thread_ts):
    assert text == "Tracking for following tests:\n*test* (2100-01-01 00:00:00)\n"
    return {"ok": "ok"}


def load_for_user(user):
    return [{"test": "test", "expiry": "2100-01-01 00:00:00"}]
