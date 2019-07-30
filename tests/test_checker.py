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
    br_url = "http://test-br-url?test="
    count = 1
    check_tests_delay = 7200
    client = type("", (), {})()
    client.chat_postMessage = post_message
    send_track(track, count, check_tests_delay, client, br_url)


def post_message(channel, text, thread_ts):
    assert text == "Test *test* failed *1x* in the last 2 hours\nhttp://test-br-url?test=test"


def test_send_track_no_br_url():
    track = {}
    track["test"] = "test"
    track["channel_id"] = "test"
    track["thread_ts"] = "test"
    track["user"] = "test"
    br_url = None
    count = 1
    check_tests_delay = 3600
    client = type("", (), {})()
    client.chat_postMessage = post_message_no_br_url
    send_track(track, count, check_tests_delay, client, br_url)


def post_message_no_br_url(channel, text, thread_ts):
    assert text == "Test *test* failed *1x* in the last 1 hour\n"
