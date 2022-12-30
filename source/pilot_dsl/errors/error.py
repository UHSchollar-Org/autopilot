
class parse_error(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message
        super().__init__(self.message)
        
class runtime_error(Exception):
    def __init__(self, token, message) -> None:
        self.token = token
        self.message = message
        super().__init__(self.message)

class return_error(runtime_error):
    """
    This is not exactly an error.
    It is used to return values from a pilang function.
    """
    def __init__(self, value) -> None:
        super().__init__(None, None)
        self.value = value