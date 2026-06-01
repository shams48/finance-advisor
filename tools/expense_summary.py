"""
tools/expense_summary.py
Tool that retrieves and formats monthly spending totals by category.
Called when the agent detects a summary or spending query.
"""

from database import get_monthly_summary
from datetime import datetime


def get_summary(user_id: str, year_month: str = None) -> str:
    """
    Get a formatted spending summary for the current or specified month.

    Args:
        user_id: The user's identifier.
        year_month: Month in YYYY-MM format. Defaults to current month.

    Returns:
        Formatted summary string for use in Claude prompt context.
    """
    if year_month is None:
        year_month = datetime.today().strftime("%Y-%m")

    results = get_monthly_summary(user_id, year_month)

    if not results:
        return f"No expenses recorded for {year_month}."

    lines = [f"Spending summary for {year_month}:"]
    total = 0.0
    for category, amount in results:
        lines.append(f"  - {category.capitalize()}: €{amount:.2f}")
        total += amount
    lines.append(f"  Total: €{total:.2f}")

    return "\n".join(lines)
