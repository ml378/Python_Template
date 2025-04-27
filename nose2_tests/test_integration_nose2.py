import unittest
from unittest.mock import Mock

from src.calculator import Calculator
from src.logger import Logger
from src.notifier import Notifier


class TestIntegrationNose2(unittest.TestCase):

    def test_calculator_logger(self):
        calculator = Calculator()
        logger = Logger()
        result = calculator.add(4, 6)
        logger.log("add", result)

        self.assertIn("add: 10", logger.get_logs())

    def test_logger_notifier(self):
        logger = Logger()
        notifier = Notifier(threshold=10)
        logger.log("multiply", 12)

        self.assertTrue(notifier.notify(12))

    def test_calculator_logger_mock_notifier(self):
        calculator = Calculator()
        logger = Logger()
        notifier_mock = Mock()

        result = calculator.multiply(5, 3)
        logger.log("multiply", result)
        notifier_mock.notify.return_value = result > 10

        self.assertIn("multiply: 15", logger.get_logs())
        self.assertTrue(notifier_mock.notify(result))

if __name__ == "__main__":
    unittest.main()
