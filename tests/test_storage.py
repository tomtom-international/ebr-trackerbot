#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ebr_trackerbot` package."""

import sys
import os

sys.path.append("ebr_trackerbot")
sys.path.append("ebr_trackerbot/storage")


def delete_fixtures():
    if os.path.exists("data.db"):
        os.unlink("data.db")
    if os.path.exists("data-odbc.db"):
        os.unlink("data-odbc.db")


def reset_fixtures():
    delete_fixtures()
    open("data-odbc.db", "a").close()


reset_fixtures()

from bot import config
from state import STATE

config["odbc_connection_string"] = "DRIVER={SQLITE3};DATABASE=data-odbc.db"

import pytest
import sqlite
import memory
import odbc


def test_storage():
    modules = ["memory"]

    for module_name in modules:
        module = None
        for storage in STATE.bot_storage:
            if storage["name"] == module_name:
                module = storage
                break
        assert len(module["load_all_tracked_tests"]()) == 0
        module["save"](
            "test-user", {"test": "abc", "expiry": "2100-01-01T00:00:00Z", "channel_id": "test", "thread_ts": "0123"}
        )
        assert len(module["load_all_tracked_tests"]()) == 1
        assert len(module["load_for_user"]("test-user")) == 1
        assert len(module["load_for_user"]("non-existing-user")) == 0
        module["delete_for_user"]("test-user", "abc")
        assert len(module["load_all_tracked_tests"]()) == 0
        assert len(module["load_for_user"]("test-user")) == 0
        module["save"](
            "test-user", {"test": "abc", "expiry": "2000-01-01T00:00:00Z", "channel_id": "test", "thread_ts": "0123"}
        )
        module["clean_expired_tracks"]()
        assert len(module["load_all_tracked_tests"]()) == 0
        assert len(module["load_for_user"]("test-user")) == 0
        module["save"](
            "test-user", {"test": "abc", "expiry": "2000-01-01T00:00:00Z", "channel_id": "test", "thread_ts": "0123"}
        )
        module["save"](
            "test-user", {"test": "abc", "expiry": "2100-01-01T00:00:00Z", "channel_id": "test2", "thread_ts": "01234"}
        )
        assert module["load_for_user"]("test-user")[0]["expiry"] == "2100-01-01T00:00:00Z"
        module["save"](
            "test-user", {"test": "abc2", "expiry": "2100-01-01T00:00:00Z", "channel_id": "test2", "thread_ts": "01234"}
        )
        assert len(module["load_for_user"]("test-user")) == 2

    delete_fixtures()
