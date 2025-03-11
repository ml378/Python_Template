import pytest

from src.notifier import Notifier


@pytest.fixture
def notifier():
    return Notifier(threshold=10)

def test_notifier(notifier):
    assert notifier.notify(12) is True
    assert notifier.notify(5) is False
