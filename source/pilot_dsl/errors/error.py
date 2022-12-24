
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