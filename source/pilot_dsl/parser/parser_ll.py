from typing import List
from source.pilot_dsl.lexer.token_ import token
from source.pilot_dsl.lexer.static_data import token_type
from source.pilot_dsl.ast.expressions import *
from source.pilot_dsl.errors.error import *

"""Grammar:

    expression  ->  equality
    equality    ->  comparison (( "!=" | "==" ) comparison)*
    comparison  ->  term (( ">" | ">=" | "<" | "<=" ) term)*
    term        ->  factor (( "-" | "+" ) factor)*
    factor      ->  unary (( "/" | "*" ) unary)*
    unary       ->  ( "!" | "-" ) unary | primary
    primary     ->  Number | String | "true" | "false" | "null" | "(" expression ")"  
    
"""

class parser_ll:
    def __init__(self, tokens : List[token], on_token_error = None) -> None:
        self.tokens = tokens
        self.on_token_error = on_token_error
        self.current = 0
    
    def prev(self) -> token:
        return self.tokens[self.current - 1]
    
    def peek(self) -> token:
        return self.tokens[self.current]
    
    def is_at_end(self) -> bool:
        return self.peek().type == token_type.EOF
    
    def advance(self) -> token:
        if not self.is_at_end():
            self.current += 1
        return self.prev()
    
    def check(self, type : token_type) -> bool:
        if self.is_at_end():
            return False
        
        return self.peek().type == type
    
    def match(self, *types : token_type) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        
        return False
    
    def _expression(self) -> expression:
        return self._equality()
    
    def _equality(self) -> expression:
        exp = self._comparison()
        
        while self.match(token_type.NOT_EQUAL, token_type.EQUAL_EQUAL):
            op : token = self.prev()
            right : expression = self._comparison()
            exp = binary_exp(exp, right, op)
        
        return exp
    
    def _comparison(self) -> expression:
        exp = self._term()
        
        while self.match(token_type.GREATER, token_type.GREATER_EQUAL, token_type.LESS, token_type.LESS_EQUAL):
            op : token = self.prev()
            right : expression = self._term()
            exp = binary_exp(exp, right, op)
        
        return exp
    
    def _term(self) -> expression:
        exp = self._factor()
        
        while self.match(token_type.MINUS, token_type.PLUS):
            op : token = self.prev()
            right : expression = self._factor()
            exp = binary_exp(exp, right, op)
        
        return exp
    
    def _factor(self) -> expression:
        exp = self._unary()
        
        while self.match(token_type.SLASH, token_type.ASTERISK):
            op : token = self.prev()
            right : expression = self._unary()
            exp = binary_exp(exp, right, op)
        
        return exp

    def _unary(self) -> expression:
        if self.match(token_type.NOT, token_type.MINUS):
            op : token = self.prev()
            right : expression = self._unary()
            return unary_exp(op, right)
        
        return self._primary()

    def _primary(self) -> expression:
        if self.match(token_type.FALSE):
            return literal_exp(False)
        
        if self.match(token_type.TRUE):
            return literal_exp(True)
        
        if self.match(token_type.NULL):
            return literal_exp(None)
        
        if self.match(token_type.NUMBER, token_type.STRING):
            return literal_exp(self.prev().literal)
        
        if self.match(token_type.LEFT_PAREN):
            exp : expression = self._expression()
            self.consume(token_type.RIGHT_PAREN, "Expect ')' after expression.") #here we find an parsing error
            return grouping_exp(exp)
        
        raise self._error(self.peek(), "Expect expression.")
    
    def consume(self, token_type, error_msg):
        if self.check(token_type):
            return self.advance()
        
        self._error(self.peek(), error_msg) ## here we find an parsing error
    
    def _error(self, token : token, msg : str):
        self.on_token_error(token, msg)
        raise parse_error(token, msg)
    
    def synchronize(self):
        self.advance()
        
        while not self.is_at_end():
            if self.prev().type == token_type.SEMICOLON:
                return
            
            if self.peek().type in [
                token_type.CLASS,
                token_type.FUN,
                token_type.VAR,
                token_type.FOR,
                token_type.IF,
                token_type.WHILE,
                token_type.PRINT,
                token_type.RETURN
            ]:
                return
            
            self.advance()
    
    def parse(self):
        
        try:
            return self._expression()
        except parse_error:
            return None