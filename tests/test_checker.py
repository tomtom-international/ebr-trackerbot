#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ebr_trackerbot` package."""

import sys
import os

sys.path.append("ebr_trackerbot")

import pytest
from checker import send_track


def test_send_track():
    track = {}
    track["test"] = "test"
    track["channel_id"] = "test"
    track["thread_ts"] = "test"
    track["user"] = "test"
    count = 1
    check_tests_delay = 7200
    client = type("", (), {})()
    client.chat_postMessage = post_message
    send_track(
        track,
        count,
        check_tests_delay,
        client,
        "Test *{{test}}* failed *{{count}}x* in the last {{period}}\nhttp://test-url?test={{test}}",
    )


def post_message(channel, text, thread_ts):
    assert text == "Test *test* failed *1x* in the last 2 hours\nhttp://test-url?test=test"


def test_send_track_no_custom_slack_message():
    track = {}
    track["test"] = "test"
    track["channel_id"] = "test"
    track["thread_ts"] = "test"
    track["user"] = "test"
    count = 1
    check_tests_delay = 3600
    client = type("", (), {})()
    client.chat_postMessage = post_message_no_custom_slack_message
    send_track(track, count, check_tests_delay, client, None)


def post_message_no_custom_slack_message(channel, text, thread_ts):
    assert text == ""
