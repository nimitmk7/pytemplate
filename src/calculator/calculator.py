"""This module provides a simple calculator implementation."""
import calculator_interface

"""This is the class that implements the calculator interface."""
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
        """Divide two numbers, while making sure to avoid division by zero, 
        and return the result."""
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b