from .static_data import token_type

class token:
    def __init__(self, token_type : token_type, lexeme : str, literal, line : str) -> None:
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    
    def __str__(self) -> str:
        return f'{self.type} {self.lexeme} {self.literal}'
    
    def __repr__(self) -> str:
        return self.__str__()
