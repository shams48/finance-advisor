"""
database.py
Handles all SQLite database operations for the AI Personal Finance Advisor.
Creates and manages the expenses table.
"""

import sqlite3
from datetime import datetime


DB_FILE = "finance.db"


def get_connection():
    """Return a connection to the SQLite database."""
    return sqlite3.connect(DB_FILE)


def initialize_db():
    """Create the expenses table if it does not exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def insert_expense(user_id: str, amount: float, category: str, date: str = None):
    """
    Insert a new expense record into the database.
    
    Args:
        user_id: Identifier for the user.
        amount: Expense amount in euros.
        category: Expense category (e.g. food, transport).
        date: Date string in YYYY-MM-DD format. Defaults to today.
    
    Returns:
        True if successful, False otherwise.
    """
    if date is None:
        date = datetime.today().strftime("%Y-%m-%d")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (user_id, amount, category, date) VALUES (?, ?, ?, ?)",
            (user_id, amount, category, date)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"[DB Error] Failed to insert expense: {e}")
        return False


def get_monthly_summary(user_id: str, year_month: str = None):
    """
    Query total spending grouped by category for a given month.
    
    Args:
        user_id: Identifier for the user.
        year_month: Month in YYYY-MM format. Defaults to current month.
    
    Returns:
        List of (category, total) tuples.
    """
    if year_month is None:
        year_month = datetime.today().strftime("%Y-%m")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT category, SUM(amount)
            FROM expenses
            WHERE user_id = ? AND date LIKE ?
            GROUP BY category
        """, (user_id, f"{year_month}%"))
        results = cursor.fetchall()
        conn.close()
        return results
    except sqlite3.Error as e:
        print(f"[DB Error] Failed to fetch summary: {e}")
        return []


def get_all_expenses(user_id: str):
    """
    Retrieve all expense records for a user.
    
    Args:
        user_id: Identifier for the user.
    
    Returns:
        List of all expense rows.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, amount, category, date FROM expenses WHERE user_id = ? ORDER BY date DESC",
            (user_id,)
        )
        results = cursor.fetchall()
        conn.close()
        return results
    except sqlite3.Error as e:
        print(f"[DB Error] Failed to fetch expenses: {e}")
        return []
