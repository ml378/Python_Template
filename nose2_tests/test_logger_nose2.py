import unittest
from src.logger.logger import Logger

class TestLoggerNose2(unittest.TestCase):

    def setUp(self):
        self.logger = Logger()

    def test_logger(self):
        self.logger.log("add", 5)
        self.assertIn("add: 5", self.logger.get_logs())

if __name__ == '__main__':
    unittest.main()
