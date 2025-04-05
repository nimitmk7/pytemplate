""" This module defines the Calculator interface. """


class Calculator:
    def add(self, a, b):
        """Add two numbers and return the result.

        Args:
            a (float): The first number.
            b (float): The second number.

        Returns:
            float: The sum of a and b.
        """
        raise NotImplementedError("This method should be overridden by subclasses")

    def subtract(self, a, b):
        """Subtract two numbers and return the result.

        Args:
            a (float): The first number.
            b (float): The second number.

        Returns:
            float: The difference of a and b.
        """
        raise NotImplementedError("This method should be overridden by subclasses")

    def multiply(self, a, b):
        """Multiply two numbers and return the result.

        Args:
            a (float): The first number.
            b (float): The second number.

        Returns:
            float: The product of a and b.
        """
        raise NotImplementedError("This method should be overridden by subclasses")

    def divide(self, a, b):
        """Divide two numbers, while making sure to avoid division by zero, 
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
