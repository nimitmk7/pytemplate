"""
A definition of the Calculator interface.
Provides basic arithmetic operations.
"""

from abc import ABC, abstractmethod

class Calculator(ABC):
    @abstractmethod
    def add(self, a: float, b: float) -> float:
        """Add two numbers and return the result."""
        pass # pragma: no cover
    
    @abstractmethod
    def subtract(self, a: float, b: float) -> float:
        """Subtract two numbers and return the result."""
        pass # pragma: no cover
    
    @abstractmethod
    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers and return the result."""
        pass # pragma: no cover
    
    @abstractmethod
    def divide(self, a: float, b: float) -> float:
        """Divide two numbers and return the result."""
        pass # pragma: no cover