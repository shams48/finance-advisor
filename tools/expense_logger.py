"""
tools/expense_logger.py
Tool that logs a new expense entry into the SQLite database.
Called when the agent detects the user wants to record a purchase.
"""

from database import insert_expense


def log_expense(user_id: str, amount: float, category: str, date: str = None) -> str:
    """
    Log a new expense to the database.

    Args:
        user_id: The user's identifier.
        amount: Amount spent in euros.
        category: Category of the expense (e.g. food, transport).
        date: Optional date string YYYY-MM-DD. Defaults to today.

    Returns:
        Confirmation message string.
    """
    success = insert_expense(user_id, amount, category, date)
    if success:
        return f"Logged: €{amount:.2f} under '{category}'."
    else:
        return "Failed to log expense. Please try again."
