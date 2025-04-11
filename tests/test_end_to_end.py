from src.calculator.calculator import Calculator
from src.logger.logger import Logger
from src.notifier.notifier import Notifier


def test_end_to_end():
    calc = Calculator()
    log = Logger()
    notify = Notifier(threshold=10)

    result = calc.multiply(3, 4)
    log.log("multiply", result)
    notification_sent = notify.notify(result)

    assert "multiply: 12" in log.get_logs()
    assert notification_sent is True
