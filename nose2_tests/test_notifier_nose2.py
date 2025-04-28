import unittest

from src.notifier import Notifier


class TestNotifierNose2(unittest.TestCase):
    def setUp(self):
        self.notifier = Notifier(threshold=10)

    def test_notifier(self):
        self.assertTrue(self.notifier.notify(12))
        self.assertFalse(self.notifier.notify(5))


if __name__ == "__main__":
    unittest.main()
