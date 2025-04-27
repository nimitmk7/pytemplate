# Component Documentation

This document defines the structure, naming conventions, and guidelines for components in this repository. Components are self-contained modules that encapsulate specific functionality behind a clear, minimal interface. Following these guidelines ensures that our components are easy to understand, maintain, and test while hiding internal complexity.

---

## 1. Component Structure

Each component should be organized within its own subdirectory under the `src` directory.

- **Directory Structure:**
  The component’s header and implementation files should reside in a subdirectory whose name matches the component. For example, for a component named **Calculator**, the structure should be:

```
src/
    └── calculator/
        ├── calculator_interface.py
        ├── calculator.py
        └── tests/  # unit tests for the component
              
```

- **Interface Files:**
Interface files should be named after the classes or functionalities they declare and placed within the component's directory (e.g., `src/calculator/calculator_interface.py`).

- **Implementation Files:**
Implementation files should correspond to their header files and be placed within the same component directory (e.g., `src/calculator/calculator.py`).

---

## 2. Naming Conventions

- **Classes:** Use lowercase letters with words separated by underscores.
*Example:* `calculator`, `logger`, `notifier`

- **Functions/Variables:** Use camelCase.
*Example:* `add`, `subtract`, `logOperation`

---

## 3. Documentation Guidelines

- **Component-Level Documentation:**
Each component should have a leading comment block in its interface file that describes its purpose and main functionalities.

- **Public Interface Documentation:**
Public classes, methods, and functions must be documented in the interface files. Documentation should include:
  - A brief description of what the method or class does.
  - Descriptions of parameters.
  - The return value.
  - Any exceptions thrown.

- **Design Intent:**
Document design decisions that hide internal complexity and promote modularity. This allows users of the component to interact with it through a simple, clear interface without needing to know internal details.

---

## 4. Consistency and Isolation

- **Consistency:**
Ensure that naming, file structure, and documentation are consistent within and across components to improve readability and maintainability.

- **Isolation:**
Design components to minimize dependencies on other components. Use forward declarations and abstract interfaces where possible to reduce coupling.

---

## 5. Testing

- Each component must have corresponding unit tests.
- Create a `tests` subdirectory within each component’s directory (e.g., `src/calculator/tests/`).
- Test files should follow the same naming conventions and aim for comprehensive coverage of the component's functionality.
- Integration and End-to-End Tests must be in the root test directory (e.g., `~/tests/e2e/`).

---

## 6. Example: Calculator Component

Below is an example of how the calculator component might be structured and documented.

### Example Interface File: `src/calculator/calculator_interface.py`

```py
"""A definition of the Calculator interface.
Provides basic arithmetic operations."""


class Calculator:
    def add(self, a: float, b: float) -> float:
        """Add two numbers and return the result.

        Args:
            a (float): The first number.
            b (float): The second number.

        Returns:
            float: The sum of a and b.
        """
        raise NotImplementedError("This method should be overridden by subclasses")

    def subtract(self, a: float, b: float) -> float:
        """Subtract two numbers and return the result.

        Args:
            a (float): The first number.
            b (float): The second number.

        Returns:
            float: The difference of a and b.
        """
        raise NotImplementedError("This method should be overridden by subclasses")

    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers and return the result.

        Args:
            a (float): The first number.
            b (float): The second number.

        Returns:
            float: The product of a and b.
        """
        raise NotImplementedError("This method should be overridden by subclasses")

    def divide(self, a: float, b: float) -> float:
        """
        Divide two numbers, while making sure to avoid division by zero, 
        and return the result.

        Args:
            a (float): The first number.
            b (float): The second number.

        Returns:
            float: The quotient of a and b.

        Raises:
            ValueError: If b is zero.
        """
        raise NotImplementedError("This method should be overridden by subclasses")

```

### Example Implementation File: `src/calculator/calculator.py`

```py
"""Provides implmentation of the calculator interface."""
from . import calculator_interface

class Calculator(calculator_interface.Calculator):
    def add(self, a: float, b: float) -> float:
        """Add two numbers and return the result."""
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Subtract two numbers and return the result."""
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers, and return the result."""
        return a * b

    def divide(self, a:float, b:float) -> float:
        """
        Divide two numbers, while making sure to avoid division by zero, 
        and returns the result.
        """
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b

```

## Components in this Repository

### Calculator

- **Purpose:** Performs basic arithmetic operations.
- **Interface:**
  - `def add(self, a: float, b: float) -> float`
  - `def subtract(self, a: float, b: float) -> float`
  - `multiply(self, a: float, b: float) -> float`
  - `divide(self, a:float, b:float) -> float` (throws an exception on division by zero)


### Logger

- **Purpose:** Records operations performed by calculator.
- **Interface:**
  - `def __init__(self) -> None`
  - `def log(self, message: str) -> None`
  - `def get_logs(self) -> list[str]`


### Notifier

- **Purpose:** Monitors calculation results and triggers notifications if a result exceeds a predefined threshold.
- **Interface:**
  - `def check_and_notify(self, value: float) -> None`
  - `def was_notified(self) -> bool`