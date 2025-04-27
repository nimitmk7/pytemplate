# AI Conversation Client - Implementation

This project implements a modular AI Conversation Client in Python.  
It connects to AI providers (here we use OpenAI) and manages conversation threads in a clean, scalable, and testable way.

## Project Structure

```
src/
├── ai_conversation_client/            # Abstract Interfaces (HW2)
│   ├── __init__.py
│   ├── interfaces.py
│   └── tests/
│       └── unit/
│           └── test_interfaces.py
├── ai_conversation_client_impl/       # Concrete Implementations (HW3)
│   ├── __init__.py
│   ├── client.py                      # Main implementation
│   └── tests/
│       ├── unit/
│           ├── test_openai_provider.py
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

Make sure you have a `.env` file or set your OpenAI API key:
```bash
OPENAI_API_KEY=your-openai-api-key
```

## Components

| Component | Description |
|:---|:---|
| `OpenAIProvider` | Connects to the OpenAI API and fetches model completions. |
| `ConcreteThread` | Represents an individual conversation thread with a model and message history. |
| `ConcreteThreadRepository` | Stores, retrieves, updates, and deletes conversation threads in memory. |
| `ConcreteAIConversationClient` | Public client API for managing threads, posting messages, updating models, and interacting with the provider. |

## Features

- **Thread Management**: Create, retrieve, list, and delete conversation threads.
- **Model Management**: Update thread models dynamically.
- **Messaging**: Post a message and get AI-generated responses.
- **Provider Integration**: Plug in OpenAI (extendable for other providers).
- **Error Handling**: Raise `ValueError` for invalid operations.
- **Extensible Design**: Easily swap in new providers or repositories.

## Running Tests

```bash
# Run all tests
pytest src

# Check coverage
pytest --cov=src

# Linting and static checks
uvx ruff check .
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

To check CI locally:

```bash
# Ruff (formatting)
uvx ruff check .

# Mypy (typing)
uvx mypy .

# Pytest (tests)
pytest src --cov=src
```

## Notes

- Unit tests are separated from integration tests.
- Dummy mocks are used for unit tests to avoid real API calls.
- Integration tests test the full working of ConcreteAIConversationClient.
- API errors (e.g., invalid models, missing threads) are properly surfaced.


