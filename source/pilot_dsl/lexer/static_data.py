from enum import Enum, auto, unique
from typing import Dict

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
    #REMAINDER = auto(),
    #endregion
    
    #region One or two character tokens.
    NOT = auto(),
    NOT_EQUAL = auto(),
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
    CLASS = auto(),
    FATHER = auto(),
    #endregion
    
    EOF = auto()

keywords_map : Dict[str, token_type] = {
    'and': token_type.AND,
    'if' : token_type.IF,
    'else': token_type.ELSE,
    'fun' : token_type.FUN,
    'for' : token_type.FOR,
    'null' : token_type.NULL,
    'or' : token_type.OR,
    'print' : token_type.PRINT,
    'return' : token_type.RETURN,
    'this' : token_type.THIS,
    'true' : token_type.TRUE,
    'false' : token_type.FALSE,
    'var' : token_type.VAR,
    'while' : token_type.WHILE,
    'class' : token_type.CLASS,
    'father' : token_type.FATHER }
