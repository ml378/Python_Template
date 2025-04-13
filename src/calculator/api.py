"""Simple Calculator module for basic aarithmetic."""

from src.calculator.calculator import Calculator

# Instantiate the calculator
_calculator = Calculator()

def add(a: float, b: float) -> float:
    """Add two numbers."""
    return _calculator.add(a, b)

def subtract(a: float, b: float) -> float:
    """Subtract two numbers."""
    return _calculator.subtract(a, b)

def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return _calculator.multiply(a, b)

def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    return _calculator.divide(a, b)

# Define the public API of this module
__all__ = ["add", "subtract", "multiply", "divide"]

