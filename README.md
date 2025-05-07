# Mail-AI Spam Detection App

This project implements a Gmail email crawler combined with an AI-powered spam detection client. It integrates a custom Gmail client and a conversation AI (Gemini) to classify incoming emails based on spam probability.

---

## Project Structure

```
src/
├── mail_ai_app/                  # Main mail AI application
│   ├── __init__.py
│   ├── main.py                   # Main entry point for email crawling and spam detection
│   ├── prompt_utils.py           # Utilities for prompt construction and processing
│   └── tests/                    # Unit and integration tests for mail_ai_app
│       ├── test_main.py
│       └── test_prompt_utils.py
tests/
├── unit/
│   ├── test_mail_ai_app.py
│   └── test_other_modules.py
└── e2e/
    └── test_integration_mail_ai.py    # End-to-end integration test for mail AI app
external/
└── gmail_client/                 # External Gmail client submodule
```

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd <your-repo-directory>

# Set up a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install uv and dev dependencies
curl -LsSf https://astral.sh/uv/install.sh | sh
uv pip install -e ".[dev]"
```

Create a `.env` file at the root with your Gemini API key:

```bash
GEMINI_API_KEY=your-gemini-api-key
```

Or export it manually:

```bash
export GEMINI_API_KEY=your-gemini-api-key
```

## Components

The Mail-AI application consists of the following key components inside `mail_ai_app/`:

- `main.py`: The main script that crawls Gmail inbox emails, sends them to the AI conversation client for spam probability estimation, and outputs results to a CSV file.
- `prompt_utils.py`: Helper functions for constructing prompts and processing AI responses related to spam detection.
- `tests/`: Contains unit and integration tests ensuring the correctness of the mail AI app functionality.

## Main Application: Email Spam Detection

The main application crawls Gmail inbox emails and sends each email to the AI conversation client to estimate the probability of being spam. It outputs a CSV file named `email_spam_analysis.csv` containing the following columns: `mail_id`, `Pct_spam`, `subject`, and `date`.

## Running the Main App

```bash
# Ensure environment variables are set
export GEMINI_API_KEY=your-gemini-api-key
export TEST_EMAIL=your-email@gmail.com

# Run the main app
python src/mail_ai_app/main.py
```

After running the application, you will be prompted to enter how many emails to process. Upon completion, an `email_spam_analysis.csv` file will be generated containing columns: `mail_id`, `Pct_spam`, `subject`, and `date`.

## Features

- Crawl Gmail inbox emails using the Gmail client.
- Send each email content to the AI conversation client to predict spam probability.
- Aggregate and export the analysis results to a CSV file for further inspection.

## Running Tests

```bash
# Run all tests
pytest src

# Check coverage
pytest --cov=src
```

## Linting and Static Checks

```bash
# Ruff (formatting)
uvx ruff check .

# Mypy (static type checking)
uvx mypy .
```

All tests must pass and coverage should remain **≥ 90%**.

## Continuous Integration

- **CircleCI** is configured to run on every commit.
- It runs:
  - Ruff formatting check
  - Mypy static type checking
  - Pytest unit and integration tests
  - Coverage report (threshold enforced)

To run CI checks locally:

```bash
uvx ruff check .
uvx mypy .
pytest src --cov=src
```

## Notes

- Unit tests are separated from integration tests.
- Dummy mocks are used for unit tests to avoid real API calls.
- Integration tests test the full working of `ConcreteAIConversationClient`.
- API errors (e.g., invalid models, missing threads) are properly surfaced.
- GeminiProvider reads API key from the environment with fallback for testing.
- Public API (`api.py`) and Factory (`factory.py`) layers are added for clean integration into larger applications as part of HW4.
