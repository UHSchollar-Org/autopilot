from .token_ import token
from typing import List, Dict
from .static_data import token_type, keywords_map

class lexer:
    
    def __init__(self, pilang_src : str, on_error = None) -> None:
        self.on_error = on_error
        self.source = pilang_src
        self.tokens : List[token] = []
        self.start = self.current_pos = 0
        self.line = 1
        self.tokenize()
        
    
    def add_token(self, token_type, literal = None):
        text = self.source[self.start : self.current_pos]
        self.tokens.append(token(token_type, text, literal, self.line))
    
    def is_at_end(self) -> bool:
        return self.current_pos >= len(self.source)
    
    def match(self, expected) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current_pos] != expected:
            return False
        self.current_pos += 1
        return True
    
    def peek(self):
        if self.is_at_end():
            return '\0'
        else:
            return self.source[self.current_pos]
    
    def consume_str(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            
            self.current_pos += 1
            
        if self.is_at_end():
            # throw an Unterminated string error in line self.line
            # and return
            self.on_error(self.line, "Unterminated string")
            return
        #here we find "
        self.current_pos += 1
        
        string = self.source[self.start + 1: self.current_pos - 1]
        
        self.add_token(token_type.STRING, string)
    
    def peek_next(self) -> str:
        if self.current_pos + 1 >= len(self.source):
            return '\0'
        return self.source[self.current_pos + 1]
    
    def consume_number(self):
        while self.peek().isdigit():
            self.current_pos += 1
        
        # maybe is a fractional number, so we ask for a .
        if self.peek() == '.' and self.peek_next().isdigit():
            self.current_pos += 1
            
            while self.peek().isdigit():
                self.current_pos += 1
        
        self.add_token(token_type.NUMBER, float(self.source[self.start : self.current_pos]))
         
    def consume_identifier(self):
        while self.peek().isalnum():
            self.current_pos += 1
        
        text = self.source[self.start:self.current_pos]
        
        t_type = keywords_map.get(text, token_type.IDENTIFIER)
        
        self.add_token(t_type)
    
    def consume_token(self):
        self.current_pos += 1
        char = self.source[self.current_pos - 1]
        
        match char:
            case '(':
                self.add_token(token_type.LEFT_PAREN)
            case ')':
                self.add_token(token_type.RIGHT_PAREN)
            case '{':
                self.add_token(token_type.LEFT_BRACE)
            case '}':
                self.add_token(token_type.RIGHT_BRACE)
            case ',':
                self.add_token(token_type.COMMA)
            case '.':
                self.add_token(token_type.DOT)
            case '-':
                self.add_token(token_type.MINUS)
            case '+':
                self.add_token(token_type.PLUS)
            case ';':
                self.add_token(token_type.SEMICOLON)
            case '*':
                self.add_token(token_type.ASTERISK)
            case'!':
                self.add_token(token_type.NOT_EQUAL if self.match('=') else token_type.NOT)
            case '=':
                self.add_token(token_type.EQUAL_EQUAL if self.match('=') else token_type.EQUAL)
            case '<':
                self.add_token(token_type.LESS_EQUAL if self.match('=') else token_type.LESS)
            case '>':
                self.add_token(token_type.GREATER_EQUAL if self.match('=') else token_type.GREATER)
            case '/':
                if self.match('/'):
                    #here we find a comment and we ignore the rest of the line
                    while self.peek() != '\n' and not self.is_at_end():
                        self.current_pos += 1
                else:
                    self.add_token(token_type.SLASH)
            case ' ':
                #ignore whitespace
                pass 
            case '\r':
                #ignore carriage return
                pass 
            case '\t':
                #ignore tab
                pass 
            case '\n':
                #increment line number
                self.line += 1 
            case '"':
                #here we find a string and we need to consume it
                self.consume_str() 
            case _:
                if char.isdigit():
                    #here we find a number and we need to consume it
                    self.consume_number()
                elif char.isalpha():
                    #here we find an identifier and we need to consume it
                    self.consume_identifier() 
                elif self.on_error:
                    # throw an Unexpected character error in line self.line
                    # and continue scanning to find other potencial errors
                    self.on_error(self.line, f'Unexpected character: {char}')
                else:
                    raise
    
    def tokenize(self):
        
        while not self.is_at_end():
            self.start = self.current_pos 
            self.consume_token()
        
        self.tokens.append(token(token_type.EOF, '', None, self.line))
        
        return self.tokens