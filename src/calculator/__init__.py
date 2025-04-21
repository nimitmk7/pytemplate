"""API for the calculator component.

This module provides a simple API for basic arithmetic operations.
"""

from .calculator import Calculator
from .calculator_interface import Calculator as CalculatorInterface

_calculator = Calculator()

# Exposing API functions
def add(a: float, b: float) -> float:
    """Add two numbers and return the result."""
    return _calculator.add(a, b)

def subtract(a: float, b: float) -> float:
    """Subtract two numbers and return the result."""
    return _calculator.subtract(a, b)

def multiply(a: float, b: float) -> float:
    """Multiply two numbers and return the result."""
    return _calculator.multiply(a, b)

def divide(a: float, b: float) -> float:
    """Divide two numbers and return the result."""
    return _calculator.divide(a, b)

__all__ = ["add", "subtract", "multiply", "divide", "Calculator", "CalculatorInterface"]