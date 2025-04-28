class Logger:
    def __init__(self):
        self.logs = []

    def log(self, operation: str, result: float):
        self.logs.append(f"{operation}: {result}")

    def get_logs(self):
        return self.logs
