class SolverError(Exception):
    def __init__(self, message: str = "Unexpected solver error"):
        self.message = message
        super().__init__(self.message)
