"""
tests/test_agent.py
Tests for agent.py intent classification and expense extraction.
These tests do NOT call the Claude API — they test local logic only.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent import classify_intent, extract_expense


# --- Intent classification tests ---

def test_classify_log_spent():
    assert classify_intent("I spent €12 on lunch today") == "log"


def test_classify_log_bought():
    assert classify_intent("I bought a book for 8 euros") == "log"


def test_classify_log_paid():
    assert classify_intent("Paid 5.50 for coffee") == "log"


def test_classify_summary_show():
    assert classify_intent("Show my spending this month") == "summary"


def test_classify_summary_how_much():
    assert classify_intent("How much did I spend this week?") == "summary"


def test_classify_advice_default():
    assert classify_intent("Am I saving enough money?") == "advice"


def test_classify_advice_general():
    assert classify_intent("Give me some budget tips") == "advice"


# --- Expense extraction tests ---

def test_extract_amount_basic():
    amount, _ = extract_expense("I spent 12 euros on food")
    assert amount == 12.0


def test_extract_amount_decimal():
    amount, _ = extract_expense("Paid 5.50 for coffee")
    assert amount == 5.50


def test_extract_category_food():
    _, category = extract_expense("I spent 10 on lunch")
    assert category == "food"


def test_extract_category_transport():
    _, category = extract_expense("Paid 3 for the bus")
    assert category == "transport"


def test_extract_category_entertainment():
    _, category = extract_expense("Bought a movie ticket for 8 euros")
    assert category == "entertainment"


def test_extract_category_default_other():
    _, category = extract_expense("Spent 20 on something random")
    assert category == "other"


def test_extract_no_amount_returns_zero():
    amount, _ = extract_expense("I bought something")
    assert amount == 0.0
