from unittest.mock import Mock

from src.calculator import Calculator
from src.logger import Logger
from src.notifier import Notifier


def test_calculator_logger():
    calculator = Calculator()
    logger = Logger()
    result = calculator.add(4, 6)
    logger.log("add", result)
    assert "add: 10" in logger.get_logs()


def test_logger_notifier():
    logger = Logger()
    notifier = Notifier(threshold=10)
    logger.log("multiply", 12)
    assert notifier.notify(12) is True


def test_calculator_logger_mock_notifier():
    calculator = Calculator()
    logger = Logger()
    notifier_mock = Mock()

    result = calculator.multiply(5, 3)
    logger.log("multiply", result)
    notifier_mock.notify.return_value = result > 10

    assert "multiply: 15" in logger.get_logs()
    assert notifier_mock.notify(result) is True
