#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ebr_trackerbot` package."""

import os
import logging
import ebr_trackerbot.storage.db as db
from unittest.mock import Mock


def test_storage_db_create_table():
    conn = Mock()
    executeMock = Mock()
    conn.cursor.return_value = executeMock

    db.create_table(lambda: conn)

    conn.cursor.assert_called_once()
    executeMock.execute.assert_called_once_with(
        "CREATE TABLE IF NOT EXISTS tracks (id integer PRIMARY KEY, user text NOT NULL, test text NOT NULL,  expiry timestamp NOT NULL, channel_id text NOT NULL, thread_ts text NOT NULL);"
    )


def test_storage_db_create_table_exception(caplog):
    conn = Mock()
    conn.cursor.side_effect = Mock(side_effect=Exception("TestException"))

    with caplog.at_level(logging.ERROR):
        db.create_table(lambda: conn)

    conn.close.assert_called_once()
    assert "TestException" in caplog.text


def test_storage_db_delete_for_user():
    conn = Mock()
    executeMock = Mock()
    conn.cursor.return_value = executeMock

    db.delete_for_user(lambda: conn, "test-user", "test")

    conn.cursor.assert_called_once()
    executeMock.execute.assert_called_once_with(
        " DELETE FROM tracks WHERE user = ? AND test = ?; ", ["test-user", "test"]
    )


def test_storage_db_save_no_existing_record():
    conn = Mock()
    executeMock = Mock()
    conn.cursor.return_value = executeMock
    executeMock.fetchall.return_value = []

    db.save(
        lambda: conn,
        "test-user",
        {"test": "test", "expiry": "expiry", "channel_id": "channel_id", "thread_ts": "thread_ts"},
    )

    conn.cursor.assert_called_once()
    executeMock.execute.assert_any_call(
        " SELECT expiry, channel_id, thread_ts FROM tracks WHERE user = ? AND test = ? ", ["test-user", "test"]
    )
    executeMock.execute.assert_any_call(
        " INSERT INTO tracks (user, test, expiry, channel_id, thread_ts) VALUES (?, ?, ?, ?, ?); ",
        ["test-user", "test", "expiry", "channel_id", "thread_ts"],
    )


def test_storage_db_save_existing_record():
    conn = Mock()
    executeMock = Mock()
    conn.cursor.return_value = executeMock
    executeMock.fetchall.return_value = ["some record"]

    db.save(
        lambda: conn,
        "test-user",
        {"test": "test", "expiry": "expiry", "channel_id": "channel_id", "thread_ts": "thread_ts"},
    )

    conn.cursor.assert_called_once()
    executeMock.execute.assert_any_call(
        " SELECT expiry, channel_id, thread_ts FROM tracks WHERE user = ? AND test = ? ", ["test-user", "test"]
    )
    executeMock.execute.assert_any_call(
        " UPDATE tracks SET expiry = ?, channel_id = ?, thread_ts = ? WHERE user = ? AND test = ? ",
        ["expiry", "channel_id", "thread_ts", "test-user", "test"],
    )


def test_storage_db_load_all_tracked_tests():
    conn = Mock()
    executeMock = Mock()
    conn.cursor.return_value = executeMock
    records = [
        ["test-user", "test", "expiry", "channel_id", "thread_ts"],
        ["test-user2", "test2", "expiry2", "channel_id2", "thread_ts2"],
    ]
    executeMock.fetchall.return_value = records

    assert db.load_all_tracked_tests(lambda: conn) == [
        {"user": "test-user", "test": "test", "expiry": "expiry", "channel_id": "channel_id", "thread_ts": "thread_ts"},
        {
            "user": "test-user2",
            "test": "test2",
            "expiry": "expiry2",
            "channel_id": "channel_id2",
            "thread_ts": "thread_ts2",
        },
    ]

    conn.cursor.assert_called_once()
    executeMock.execute.assert_called_once_with(" SELECT user, test, expiry, channel_id, thread_ts FROM tracks; ")


def test_storage_db_load_for_user():
    conn = Mock()
    executeMock = Mock()
    conn.cursor.return_value = executeMock
    executeMock.fetchall.return_value = [["test-user", "test", "expiry", "channel_id", "thread_ts"]]

    assert db.load_for_user(lambda: conn, "test-user") == [
        {"test": "test", "expiry": "expiry", "channel_id": "channel_id", "thread_ts": "thread_ts"}
    ]

    conn.cursor.assert_called_once()
    executeMock.execute.assert_called_once_with(
        " SELECT user, test, expiry, channel_id, thread_ts FROM tracks WHERE user = ?; ", ["test-user"]
    )


def test_storage_db_clean_expired_tracks():
    conn = Mock()
    executeMock = Mock()
    conn.cursor.return_value = executeMock

    db.clean_expired_tracks(lambda: conn)

    conn.cursor.assert_called_once()
    executeMock.execute.assert_called_once_with(" DELETE FROM tracks WHERE expiry < DATETIME('now'); ")
