class ImagickException(Exception):
    def __init__(self, message="Salary is not in (5000, 15000) range"):
        self.message = message
        super().__init__(self.message)
