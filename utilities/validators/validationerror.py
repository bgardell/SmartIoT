class ValidationError(Exception):
    def __init__(self, validationMessage):
        self.message = validationMessage