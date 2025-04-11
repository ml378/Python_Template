import unittest
from src.calculator.calculator import Calculator
from src.logger.logger import Logger
from src.notifier.notifier import Notifier

class TestEndToEndNose2(unittest.TestCase):
    
    def setUp(self):
        self.calc = Calculator()
        self.log = Logger()
        self.notify = Notifier(threshold=10)

    def test_end_to_end(self):
        result = self.calc.multiply(3, 4)
        self.log.log("multiply", result)
        notification_sent = self.notify.notify(result)

        self.assertIn("multiply: 12", self.log.get_logs())
        self.assertTrue(notification_sent)

if __name__ == '__main__':
    unittest.main()
