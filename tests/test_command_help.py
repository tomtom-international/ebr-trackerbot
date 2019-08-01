#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ebr_trackerbot` package."""

import sys
import os

sys.path.append("ebr_trackerbot")
sys.path.append("ebr_trackerbot/command")

import pytest
from help import help_command


def test_help_empty_command():
    payload = {}
    payload["web_client"] = type("", (), {})()
    payload["web_client"].chat_postMessage = post_message_empty_commands
    payload["data"] = {}
    payload["data"]["user"] = "test"
    payload["data"]["channel"] = "test"
    payload["data"]["ts"] = "test"
    text = "help"
    result = "help"
    commands = []
    help_command(text, result, payload, commands)


def post_message_empty_commands(channel, text, thread_ts):
    assert text == "Hi <@test>! \nSupported commands:\n"
    return {"ok": "ok"}


def test_help_command():
    payload = {}
    payload["web_client"] = type("", (), {})()
    payload["web_client"].chat_postMessage = post_message_commands
    payload["data"] = {}
    payload["data"]["user"] = "test"
    payload["data"]["channel"] = "test"
    payload["data"]["ts"] = "test"
    text = "help"
    result = "help"
    commands = [{"command": "test", "description": "some description"}]
    help_command(text, result, payload, commands)


def post_message_commands(channel, text, thread_ts):
    assert text == "Hi <@test>! \nSupported commands:\n*test* some description\n"
    return {"ok": "ok"}


def test_help_failed_command():
    payload = {}
    payload["web_client"] = type("", (), {})()
    payload["web_client"].chat_postMessage = post_message_failed_commands
    payload["data"] = {}
    payload["data"]["user"] = "test"
    payload["data"]["channel"] = "test"
    payload["data"]["ts"] = "test"
    text = "help"
    result = "help"
    commands = [{"command": "test", "description": "some description"}]
    help_command(text, result, payload, commands)


def post_message_failed_commands(channel, text, thread_ts):
    return {"failed": "failed"}
