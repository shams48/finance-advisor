# AI Personal Finance Advisor

An AI-powered personal finance assistant for university students aged 18–25.
Built with Python and the Claude API (Anthropic), it lets users log daily expenses via a text-based chat interface and receive personalized budget tips based on their real spending data.

---

## Features

- Log expenses in natural language ("I spent €12 on lunch")
- Get monthly spending summaries by category
- Receive personalized AI budget advice based on real spending data
- Expenses stored locally in SQLite database
- Secure API key management via `.env` file

---

## Project Structure

```
finance_advisor/
│
├── main.py              # Entry point — runs the chat loop
├── agent.py             # Intent classification + Claude API calls
├── database.py          # SQLite operations (insert, query)
├── config.py            # Environment variable loading
│
├── tools/
│   ├── expense_logger.py    # Tool: log a new expense
│   ├── expense_summary.py   # Tool: get monthly spending summary
│   └── budget_advisor.py    # Tool: build context for Claude advice
│
├── tests/
│   ├── test_database.py     # Tests for database functions
│   ├── test_tools.py        # Tests for all three tools
│   └── test_agent.py        # Tests for intent classification + extraction
│
├── requirements.txt     # Python dependencies
├── .env.example         # Template for environment variables
└── README.md            # This file
```

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/finance-advisor.git
cd finance-advisor
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```
Open `.env` and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your_api_key_here
DEFAULT_USER_ID=student_001
MONTHLY_BUDGET=300
```

### 5. Run the application
```bash
python main.py
```

---

## Usage Examples

```
You: I spent €12 on lunch today
Advisor: Logged: €12.00 under 'food'.
         You've spent €47 on food this month...

You: Show my spending this month
Advisor: Spending summary for 2025-05:
           - Food: €47.00
           - Transport: €18.50
           Total: €65.50

You: Am I overspending?
Advisor: Based on your current spending, you have €234.50 left...
```

---

## Running Tests

```bash
pytest tests/ -v
```

No API key is required for tests — all Claude API calls are tested separately from the local logic.

---

## Deployment Strategy

This system is designed as a **local command-line application**. For wider deployment it could be wrapped in a simple web interface using Flask or FastAPI, containerized with Docker, and deployed to a cloud platform. The `.env` configuration makes it easy to adapt to different environments.

---

## Technologies Used

| Tool | Purpose |
|---|---|
| Python 3.x | Core programming language |
| Claude API (claude-sonnet) | Natural language understanding and advice |
| Anthropic Python SDK | API communication |
| SQLite (sqlite3) | Local expense storage |
| python-dotenv | Secure API key management |
| pytest | Automated testing |
