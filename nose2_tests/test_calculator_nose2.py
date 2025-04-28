import unittest

from src.calculator import Calculator


class TestCalculatorNose2(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        self.assertEqual(self.calculator.add(2, 3), 5)

    def test_subtraction(self):
        self.assertEqual(self.calculator.subtract(10, 4), 6)

    def test_multiplication(self):
        self.assertEqual(self.calculator.multiply(3, 3), 9)


if __name__ == "__main__":
    unittest.main()
