#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ebr_trackerbot` package."""

import sys
import os

sys.path.append("ebr_trackerbot")

import pytest
from bot import register_command
from bot import register_storage
from bot import get_storage
from state import STATE


def test_register_command():
    """Register command test"""
    register_command("test", "description", "regex", "callback")
    assert "test" in map(lambda x: x["command"], STATE.bot_command)


def test_register_storage():
    """Register storage test"""
    register_storage("test", "save", "load_for_user", "load_all", "delete_for_user", "clean_expired_tracks")
    assert "test" in map(lambda x: x["name"], STATE.bot_storage)


def test_get_storage():
    """Get storage test"""
    register_storage("memory", "save", "load_for_user", "load_all", "delete_for_user", "clean_expired_tracks")
    assert "save" in get_storage()
    assert "save" == get_storage()["save"]
