# Python Technology Template Repository

## Overview

This repository is a modular Python template for building component-based projects using modern development practices. It supports independent components with their own dependencies, unit and integration tests, full CI/CD setup, and type/lint/test enforcement using `uv`, `mypy`, `ruff`, `pytest`, and `coverage`.

---

## Prerequisites

This template uses [`uv`](https://github.com/astral-sh/uv) for dependency and environment management. No `pip`, `venv`, or `requirements.txt` are needed.

### Install `uv`

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/nimitmk7/pytemplate.git
cd pytemplate
```

### 2. Create and Activate Virtual Environment

```bash
uv venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
uv sync
```

---

## Code Quality and Analysis

### Run Linter (`ruff`)

```bash
uvx ruff check .
```

### Run Type Checker (`mypy`)

```bash
uvx mypy . --python-executable=$(which python)
```

---

## Running Tests

### Run All Tests with Coverage

```bash
coverage run -m pytest tests src/*/tests
coverage report -m
```

### Generate HTML Coverage Report

```bash
coverage html -d coverage-html
open coverage-html/index.html
```

### Run a Specific Test File

```bash
coverage run -m pytest src/logger/tests/test_logger.py
```

---

## Directory Structure

Each component lives in its own directory under `src/`, with colocated unit tests and an individual `pyproject.toml`.

```
src/
├── calculator/
│   ├── calculator.py
│   ├── calculator_interface.py
│   ├── pyproject.toml
│   └── tests/
├── logger/
│   ├── logger.py
│   ├── logger_interface.py
│   ├── pyproject.toml
│   └── tests/
├── notifier/
│   ├── notifier.py
│   ├── notifier_interface.py
│   ├── pyproject.toml
│   └── tests/

tests/
├── integration/
│   ├── test_calc_logger.py
│   └── test_logger_notifier.py
├── e2e/
│   └── test_e2e_full_flow.py
```

---

## Testing Strategy

### Unit Tests

Each component has its own `tests/` folder under `src/<component>/tests/`, testing that component in isolation.

### Integration Tests

Found in `tests/integration/`, these test interactions between two components:

- `test_calc_logger.py` — tests logging of calculator results
- `test_logger_notifier.py` — tests triggering notification based on logged outputs

### End-to-End (E2E) Tests

Found in `tests/e2e/`, simulating a full pipeline:

- `test_e2e_full_flow.py` — simulates calculator → logger → notifier workflow

---

## Continuous Integration with CircleCI

The pipeline (`.circleci/config.yml`) ensures:

- Linting with `ruff`
- Type checking with `mypy`
- Test running with `pytest` and `coverage`
- Test results and coverage reports are stored as **artifacts**

### Artifacts include:

- `test-results/junit.xml` — test results in JUnit format
- `coverage-html/index.html` — code coverage visual report

Artifacts can be accessed from the **Artifacts tab** in any CircleCI job page.

---

## Code Coverage in CI

To generate and upload an HTML coverage report in CircleCI, the config includes:

```yaml
      - run:
          name: Run Tests
          command: |
            coverage run -m pytest tests src/*/tests --junitxml=test-results/junit.xml
            coverage html -d coverage-html
      - store_artifacts:
          path: test-results
          destination: test-results
      - store_artifacts:
          path: coverage-html
          destination: coverage-html
```

---

## Formatting Code

To auto-format code with `ruff`:

```bash
uvx ruff format .
```

---

## Component Overview

### Calculator

- Performs basic arithmetic
- Checks division by zero
- Fully tested and type annotated

### Logger

- Logs messages into an in-memory list
- Fully type-annotated
- Interface abstraction

### Notifier

- Triggers when a value exceeds a threshold
- Tracks state using `was_notified()`

---

## Git Best Practices

- `.gitignore` excludes only relevant Python and coverage files
- No JS-related or extra entries

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.
