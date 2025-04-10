"""Logger module for logging operations."""

from .logger import Logger

# Instantiate the logger
_logger = Logger()

def log(operation: str, result: float):
    """Log an operation with its result."""
    _logger.log(operation, result)

def get_logs() -> list[str]:
    """Retrieve all logged operations."""
    return _logger.get_logs()

# Define the public API of this module
__all__ = ["log", "get_logs"]

