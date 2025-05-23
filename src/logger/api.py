"""Logger module for logging operations."""

from __future__ import annotations
from src.logger.logger import Logger
from typing import cast

# Instantiate the logger
_logger = Logger()

def log(operation: str, result: float):
    """Log an operation with its result."""
    _logger.log(operation, result)

def get_logs() -> list[str]:
    """Retrieve all logged operations."""
    return cast(list[str], _logger.get_logs())

# Define the public API of this module
__all__ = ["log", "get_logs"]

