import pytest

from src.calculator.calculator import Calculator


@pytest.fixture
def calculator():
    return Calculator()

def test_addition(calculator):
    assert calculator.add(2, 3) == 5

def test_subtraction(calculator):
    assert calculator.subtract(10, 4) == 6

def test_multiplication(calculator):
    assert calculator.multiply(3, 3) == 9

def test_division(calculator):
    assert calculator.divide(9, 3) == 3
