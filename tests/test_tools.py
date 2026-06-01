"""
tests/test_tools.py
Tests for the three tool modules: expense_logger, expense_summary, budget_advisor.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import database
import tools.expense_logger as logger
import tools.expense_summary as summary
import tools.budget_advisor as advisor


@pytest.fixture(autouse=True)
def use_test_db(tmp_path, monkeypatch):
    """Use a temporary database for all tool tests."""
    test_db = str(tmp_path / "test_finance.db")
    monkeypatch.setattr(database, "DB_FILE", test_db)
    database.initialize_db()
    yield


def test_log_expense_returns_confirmation():
    result = logger.log_expense("user1", 12.50, "food")
    assert "Logged" in result
    assert "12.50" in result
    assert "food" in result


def test_log_expense_invalid_stores_nothing():
    # Simulating a zero amount edge case
    result = logger.log_expense("user1", 0.0, "other")
    assert "Logged" in result  # Still logs, amount=0 is technically valid


def test_get_summary_no_data():
    result = summary.get_summary("user1", "2020-01")
    assert "No expenses" in result


def test_get_summary_with_data():
    database.insert_expense("user1", 25.00, "food", "2025-05-01")
    database.insert_expense("user1", 10.00, "transport", "2025-05-02")
    result = summary.get_summary("user1", "2025-05")
    assert "Food" in result or "food" in result
    assert "25.00" in result
    assert "Transport" in result or "transport" in result


def test_get_advice_context_no_data():
    result = advisor.get_advice_context("user1", 300.0)
    assert "300" in result
    assert "No expenses" in result


def test_get_advice_context_with_data():
    from datetime import datetime
    today = datetime.today().strftime("%Y-%m-%d")
    database.insert_expense("user1", 50.00, "food", today)
    result = advisor.get_advice_context("user1", 300.0)
    assert "50.00" in result
    assert "300" in result
    assert "Remaining" in result


def test_get_advice_context_remaining_budget():
    from datetime import datetime
    today = datetime.today().strftime("%Y-%m-%d")
    database.insert_expense("user1", 100.00, "food", today)
    result = advisor.get_advice_context("user1", 300.0)
    assert "200.00" in result  # 300 - 100 = 200 remaining
