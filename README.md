# AI Conversation Client - HW4 Integration Step 1: Public API and Factory Layer (Gemini Version)

This project implements a modular AI Conversation Client in Python.  
It connects to AI providers (now using **Google Gemini**) and manages conversation threads in a clean, scalable, and testable way.

## Project Structure

```
src/
├── ai_conversation_client/            # Abstract Interfaces (HW2)
│   ├── __init__.py
│   ├── interfaces.py
│   ├── api.py                     # Public API layer (HW4)
│   ├── factory.py                  # Factory layer (HW4)
│   └── tests/
│       ├── test_interfaces.py
│       ├── test_api.py             # Unit test for api.py (HW4)
│       └── test_factory.py         # Unit test for factory.py (HW4)
├── ai_conversation_client_impl/       # Concrete Implementations (HW3 with Gemini)
│   ├── __init__.py
│   ├── client.py                      # Main implementation (GeminiProvider)
│   └── tests/
│       ├── unit/
│           ├── test_gemini_provider.py
│           ├── test_repository.py
│           └── test_thread.py
│       └── integration/
│           └── test_client.py
.circleci/
    └── config.yml                      # CI pipeline
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

| Component | Description |
|:---|:---|
| `GeminiProvider` | Connects to the Gemini API and fetches model completions. |
| `ConcreteThread` | Represents an individual conversation thread with a model and message history. |
| `ConcreteThreadRepository` | Stores, retrieves, updates, and deletes conversation threads in memory. |
| `ConcreteAIConversationClient` | Public client API for managing threads, posting messages, updating models, and interacting with the provider. |
| `api.py` | Exposes a simple public API wrapping the client for easy use in apps (HW4). |
| `factory.py` | Provides a standard way to create the conversation client, wiring provider + repository (HW4). |

## Features

- **Thread Management**: Create, retrieve, list, and delete conversation threads.
- **Model Management**: Update thread models dynamically.
- **Messaging**: Post a message and get AI-generated responses.
- **Provider Integration**: Plugs into Gemini API (extensible to other providers).
- **Error Handling**: Raises `ValueError` for invalid operations.
- **Extensible Design**: Easily swap in new providers or repositories.

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
