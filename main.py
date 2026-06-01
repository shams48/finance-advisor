"""
main.py
Entry point for the AI Personal Finance Advisor.
Runs a continuous text-based chat loop for the user.
"""

from database import initialize_db
from agent import process_message
from config import DEFAULT_USER_ID


def run_chat():
    """Start the main chat loop for the finance advisor."""
    initialize_db()

    print("=" * 50)
    print("  AI Personal Finance Advisor")
    print("  Type 'exit' to quit | 'help' for tips")
    print("=" * 50)
    print()

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye! Keep tracking your spending.")
            break

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("Goodbye! Keep tracking your spending.")
            break

        if user_input.lower() == "help":
            print(
                "\nTips:\n"
                "  - Log expense:  'I spent €12 on lunch'\n"
                "  - Get summary:  'Show my spending this month'\n"
                "  - Get advice:   'Am I overspending on food?'\n"
            )
            continue

        response = process_message(user_input, DEFAULT_USER_ID)
        print(f"\nAdvisor: {response}\n")


if __name__ == "__main__":
    run_chat()
