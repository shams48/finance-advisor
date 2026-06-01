"""
tools/budget_advisor.py
Tool that prepares spending context from the database
and passes it to Claude for personalized budget advice generation.
"""

from database import get_monthly_summary
from datetime import datetime


def get_advice_context(user_id: str, monthly_budget: float = 300.0) -> str:
    """
    Build a context string summarizing the user's current spending
    to be injected into the Claude system prompt for advice generation.

    Args:
        user_id: The user's identifier.
        monthly_budget: The user's total monthly budget in euros.

    Returns:
        A formatted context string for Claude.
    """
    year_month = datetime.today().strftime("%Y-%m")
    results = get_monthly_summary(user_id, year_month)

    if not results:
        return (
            f"The user has a monthly budget of €{monthly_budget:.2f}. "
            "No expenses have been logged this month yet."
        )

    lines = [f"User's monthly budget: €{monthly_budget:.2f}"]
    lines.append(f"Spending so far this month ({year_month}):")
    total = 0.0
    for category, amount in results:
        lines.append(f"  - {category.capitalize()}: €{amount:.2f}")
        total += amount
    lines.append(f"  Total spent: €{total:.2f}")
    remaining = monthly_budget - total
    lines.append(f"  Remaining budget: €{remaining:.2f}")

    return "\n".join(lines)
