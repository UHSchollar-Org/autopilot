from enum import Enum, auto, unique

@unique
class token_type(Enum):
    #region Single-character tokens.
    LEFT_PAREN = auto(),
    RIGHT_PAREN = auto(),
    LEFT_BRACE = auto(),
    RIGHT_BRACE = auto(),
    COMMA = auto(),
    DOT = auto(),
    MINUS = auto(),
    PLUS = auto(),
    SEMICOLON = auto(),
    SLASH = auto(),
    ASTERISK = auto(),
    #endregion
    
    #region One or two character tokens.
    BANG = auto(),
    BANG_EQUAL = auto(),
    EQUAL = auto(),
    EQUAL_EQUAL = auto(),
    GREATER = auto(),
    GREATER_EQUAL = auto(),
    LESS = auto(),
    LESS_EQUAL = auto(),
    #endregion
    
    #region Literals.
    IDENTIFIER = auto(),
    STRING = auto(),
    NUMBER = auto(),
    #endregion
    
    #region Keywords.
    AND = auto(),
    IF = auto(),
    ELSE = auto(),
    FUN = auto(),
    FOR = auto(),
    NULL = auto(),
    OR = auto(),
    PRINT = auto(),
    RETURN = auto(),
    THIS = auto(),
    TRUE = auto(),
    FALSE = auto(),
    VAR = auto(),
    WHILE = auto(),
    #endregion
    
    EOF = auto()
    
class token:
    def __init__(self, token_type, lexeme, literal, line) -> None:
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    
    def __str__(self) -> str:
        return f'{self.type} {self.lexeme} {self.literal}'

