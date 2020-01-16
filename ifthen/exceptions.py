class ValidationError(Exception):
    """
    Exception class for validation error
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)
