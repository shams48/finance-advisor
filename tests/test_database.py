"""
tests/test_database.py
Unit tests for database.py functions using a temporary in-memory approach.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sqlite3
import pytest
import database


@pytest.fixture(autouse=True)
def use_test_db(tmp_path, monkeypatch):
    """Redirect database to a temporary test file."""
    test_db = str(tmp_path / "test_finance.db")
    monkeypatch.setattr(database, "DB_FILE", test_db)
    database.initialize_db()
    yield


def test_initialize_db_creates_table():
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='expenses'")
    result = cursor.fetchone()
    conn.close()
    assert result is not None


def test_insert_expense_success():
    result = database.insert_expense("user1", 12.50, "food", "2025-05-01")
    assert result is True


def test_insert_expense_stored_correctly():
    database.insert_expense("user1", 8.00, "transport", "2025-05-02")
    expenses = database.get_all_expenses("user1")
    assert len(expenses) == 1
    assert expenses[0][1] == 8.00
    assert expenses[0][2] == "transport"


def test_get_monthly_summary_correct_total():
    database.insert_expense("user1", 10.00, "food", "2025-05-01")
    database.insert_expense("user1", 20.00, "food", "2025-05-03")
    database.insert_expense("user1", 15.00, "transport", "2025-05-04")
    summary = database.get_monthly_summary("user1", "2025-05")
    summary_dict = {cat: amt for cat, amt in summary}
    assert summary_dict["food"] == 30.00
    assert summary_dict["transport"] == 15.00


def test_get_monthly_summary_empty():
    result = database.get_monthly_summary("user1", "2020-01")
    assert result == []


def test_get_all_expenses_multiple():
    database.insert_expense("user1", 5.00, "coffee", "2025-05-01")
    database.insert_expense("user1", 3.50, "transport", "2025-05-02")
    expenses = database.get_all_expenses("user1")
    assert len(expenses) == 2


def test_different_users_isolated():
    database.insert_expense("user1", 10.00, "food", "2025-05-01")
    database.insert_expense("user2", 20.00, "food", "2025-05-01")
    user1_expenses = database.get_all_expenses("user1")
    user2_expenses = database.get_all_expenses("user2")
    assert len(user1_expenses) == 1
    assert len(user2_expenses) == 1
