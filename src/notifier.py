class Notifier:
    """Sends an alert when the result exceeds a given threshold."""

    def __init__(self, threshold: float):
        self.threshold = threshold

    def notify(self, result: float) -> bool:
        return result > self.threshold
