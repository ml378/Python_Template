import pytest

from src.logger import Logger


@pytest.fixture
def logger():
    return Logger()


def test_logger(logger):
    logger.log("add", 5)
    assert "add: 5" in logger.get_logs()
