class token:
    def __init__(self, token_type, lexeme, literal, line) -> None:
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    
    def __str__(self) -> str:
        return f'{self.type} {self.lexeme} {self.literal}'
