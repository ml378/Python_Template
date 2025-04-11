"""Notifier module for exceeding the treshold limit."""

from src.notifier.notifier import Notifier

# Instantiate the notifier with a default threshold
_notifier = Notifier(threshold=10.0)

def notify(result: float) -> bool:
    """Notify if the result exceeds the threshold."""
    return _notifier.notify(result)

def set_threshold(value: float):
    """Set a new threshold for notifications."""
    _notifier.threshold = value

def get_threshold() -> float:
    """Retrieve the current threshold value."""
    return _notifier.threshold

# Define the public API of this module
__all__ = ["notify", "set_threshold", "get_threshold"]

