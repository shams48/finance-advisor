"""
agent.py
The core AI agent for the Personal Finance Advisor.
Classifies user intent and routes to the appropriate tool,
then uses Claude API to generate a natural language response.
"""

import re
import anthropic
from config import ANTHROPIC_API_KEY, DEFAULT_USER_ID, MONTHLY_BUDGET
from tools.expense_logger import log_expense
from tools.expense_summary import get_summary
from tools.budget_advisor import get_advice_context

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

CATEGORIES = ["food", "transport", "entertainment", "health",
              "shopping", "education", "utilities", "other"]


def classify_intent(user_message: str) -> str:
    """
    Classify the user's message into one of three intents:
    'log', 'summary', or 'advice'.

    Args:
        user_message: Raw text input from the user.

    Returns:
        Intent string: 'log', 'summary', or 'advice'.
    """
    message = user_message.lower()

    # Check for expense logging intent
    has_amount = bool(re.search(r'(\d+(\.\d+)?)\s*(euro|eur|€|dollars?|\$)?', message))
    log_keywords = ["spent", "bought", "paid", "purchased", "cost", "spend"]
    if has_amount and any(kw in message for kw in log_keywords):
        return "log"

    # Check for summary intent
    summary_keywords = ["summary", "show", "spent this", "how much", "overview",
                        "this week", "this month", "spending"]
    if any(kw in message for kw in summary_keywords):
        return "summary"

    # Default to advice
    return "advice"


def extract_expense(user_message: str) -> tuple:
    """
    Extract amount and category from a user message.

    Args:
        user_message: Raw text from the user.

    Returns:
        Tuple of (amount: float, category: str).
    """
    # Extract amount
    match = re.search(r'(\d+(\.\d+)?)', user_message)
    amount = float(match.group(1)) if match else 0.0

    # Extract category
    message_lower = user_message.lower()
    category = "other"
    for cat in CATEGORIES:
        if cat in message_lower:
            category = cat
            break

    # Keyword-based category hints
    food_hints = ["lunch", "dinner", "breakfast", "coffee", "restaurant",
                  "grocery", "groceries", "eat", "meal", "food"]
    transport_hints = ["bus", "tram", "taxi", "uber", "train", "fuel",
                       "petrol", "transport", "metro"]
    entertainment_hints = ["movie", "cinema", "concert", "game", "netflix",
                           "spotify", "entertainment"]

    if category == "other":
        if any(h in message_lower for h in food_hints):
            category = "food"
        elif any(h in message_lower for h in transport_hints):
            category = "transport"
        elif any(h in message_lower for h in entertainment_hints):
            category = "entertainment"

    return amount, category


def ask_claude(user_message: str, system_context: str) -> str:
    """
    Send a message to Claude API with spending context as system prompt.

    Args:
        user_message: The user's original message.
        system_context: Spending data context to guide Claude's response.

    Returns:
        Claude's text response.
    """
    try:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=512,
            system=(
                "You are a friendly AI personal finance advisor for university students. "
                "Keep responses short, practical, and encouraging. "
                "Use the spending context below to give personalized advice.\n\n"
                + system_context
            ),
            messages=[{"role": "user", "content": user_message}]
        )
        return response.content[0].text
    except anthropic.APIError as e:
        return f"[API Error] Could not reach Claude: {e}"


def process_message(user_message: str, user_id: str = None) -> str:
    """
    Main agent function. Classifies intent, calls the right tool,
    and returns a response to the user.

    Args:
        user_message: Raw input from the user.
        user_id: User identifier. Defaults to DEFAULT_USER_ID.

    Returns:
        Response string to display to the user.
    """
    if user_id is None:
        user_id = DEFAULT_USER_ID

    intent = classify_intent(user_message)

    if intent == "log":
        amount, category = extract_expense(user_message)
        if amount == 0.0:
            return "I couldn't find an amount in your message. Try: 'I spent €12 on lunch'."
        tool_result = log_expense(user_id, amount, category)
        context = get_advice_context(user_id, MONTHLY_BUDGET)
        reply = ask_claude(user_message, context)
        return f"{tool_result}\n{reply}"

    elif intent == "summary":
        tool_result = get_summary(user_id)
        context = get_advice_context(user_id, MONTHLY_BUDGET)
        reply = ask_claude(user_message, context)
        return f"{tool_result}\n{reply}"

    else:  # advice
        context = get_advice_context(user_id, MONTHLY_BUDGET)
        return ask_claude(user_message, context)
