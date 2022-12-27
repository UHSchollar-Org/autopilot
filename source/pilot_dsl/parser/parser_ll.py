from typing import List, Optional
from source.pilot_dsl.lexer.token_ import token
from source.pilot_dsl.lexer.static_data import token_type
from source.pilot_dsl.ast.expressions import *
from source.pilot_dsl.errors.error import *
from source.pilot_dsl.ast.statements import *

"""Grammar:

    program     ->  statement* EOF
    
    declaration ->  funDecl
                    | varDecl 
                    | statement
    
    funDecl     ->  "fun" function
    function    ->  IDENTIFIER "(" parameters? ")" block
    parameters  ->  IDENTIFIER ( "," IDENTIFIER )*
    varDecl     ->  "var" IDENTIFIER ("=" expression )? ";"
    
    statement   ->  exp_stmt 
                    | for_stmt
                    | if_stmt 
                    | print_stmt
                    | while_stmt 
                    | block
    
    for_stmt    ->  "for" "(" ( varDecl | exp_stmt | ";" ) expression? ";" expression? ")" statement
    while_stmt  ->  "while" "(" expression ")" statement                    
    if_stmt     ->  "if" "(" expression ")" statement ("else" statement)?
    block       ->  "{" declaration* "}"
    exp_stmt    -> expression ";"
    
    expression  ->  assignment
    
    assignment  ->  IDENTIFIER "=" assignment 
                    | logic_or
    
    logic_or    ->  logic_and ( "or" logic_and )*
    logic_and   ->  equality ( "and" equality )*
    equality    ->  comparison (( "!=" | "==" ) comparison)*
    comparison  ->  term (( ">" | ">=" | "<" | "<=" ) term)*
    term        ->  factor (( "-" | "+" ) factor)*
    factor      ->  unary (( "/" | "*" ) unary)*
    unary       ->  ( "!" | "-" ) unary
                    | call
    
    call        ->  primary ( "(" arguments? ")" )*
    arguments   ->  expression ( "," expression )*
    
    primary     ->  Number 
                    | String 
                    | "true" 
                    | "false" 
                    | "null" 
                    | "(" expression ")" 
                    | IDENTIFIER
    
    print_stmt  ->  "print" expression ";"
"""

class parser_ll:
    def __init__(self, tokens : List[token], on_token_error = None) -> None:
        self.tokens = tokens
        self.on_token_error = on_token_error
        self.current = 0
    
    #region statements
    
    def _var_declaration(self) -> statement:
        name = self.consume(token_type.IDENTIFIER, "Expect variable name.")
        
        init = None
        
        if self.match(token_type.EQUAL):
            init = self._expression()
        
        self.consume(token_type.SEMICOLON, "Expect ';' after variable declaration.")
        
        return var_stmt(name, init)
    
    def _statement(self) -> statement:
        if self.match(token_type.PRINT):
            return self._print_stmt()
        
        if self.match(token_type.LEFT_BRACE):
            return block_stmt(self._block())
        
        if self.match(token_type.IF):
            return self._if_stmt()
        
        if self.match(token_type.WHILE):
            return self._while_stmt()
        
        if self.match(token_type.FOR):
            return self._for_stmt()
        
        return self._expression_stmt()
    
    def _print_stmt(self) -> statement:
        value = self._expression()
        self.consume(token_type.SEMICOLON, f'Expect ; after {str(value)}')
        return print_stmt(value)
    
    def _expression_stmt(self) -> statement:
        exp = self._expression()
        self.consume(token_type.SEMICOLON, f'Exprect ; after {exp}')
        return expression_stmt(exp)
    
    def _block(self) -> List[statement]:
        statements = []
        
        while not self.check(token_type.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())
        
        self.consume(token_type.RIGHT_BRACE, "Expect '}' after block.")
        
        return statements
    
    def _if_stmt(self) -> statement:
        self.consume(token_type.LEFT_PAREN, "Expect '(' after 'if'.")
        condition : expression = self._expression()
        self.consume(token_type.RIGHT_PAREN, "Expect ')' after if condition.")
        
        then_branch = self._statement()
        else_branch = None
        
        if self.match(token_type.ELSE):
            else_branch = self._statement()
        
        return if_stmt(condition, then_branch, else_branch)
    
    def _while_stmt(self) -> statement:
        self.consume(token_type.LEFT_PAREN, "Expect '(' after 'while'.")
        condition : expression = self._expression()
        self.consume(token_type.RIGHT_PAREN, "Expect ')' after while condition.")
        body = self._statement()
        
        return while_stmt(condition, body)
    
    def _for_stmt(self) -> statement:
        # for_stmt using while_stmt implementation
        # for (initializer; condition; increment) body
        
        self.consume(token_type.LEFT_PAREN, "Expect '(' after 'for'.")
        
        # initializer
        if self.match(token_type.SEMICOLON):
            initializer = None
        elif self.match(token_type.VAR):
            initializer = self._var_declaration()
        else:
            initializer = self._expression_stmt()
            
        #condition
        condition = None
        if not self.check(token_type.SEMICOLON):
            condition = self._expression()
        self.consume(token_type.SEMICOLON, "Expect ';' after loop condition.")
        
        #increment
        increment = None
        if not self.check(token_type.RIGHT_PAREN):
            increment = self._expression()
        self.consume(token_type.RIGHT_PAREN, "Expect ')' after for clauses.")
        
        body = self._statement()
        
        #if increment is not None, execute it after every body call
        if increment:
            body = block_stmt([body, expression_stmt(increment)])
        
        #if condition is None, set it to True
        if condition is None:
            condition = literal_exp(True)
        
        #create a while loop with the condition and body
        body = while_stmt(condition, body)
        
        #if initializer is not None, execute it before the while loop
        if initializer is not None:
            body = block_stmt([initializer, body])
        
        return body
        
    #endregion
    
    #region expressions
    
    def _expression(self) -> expression:
        return self._assignment()
    
    def _assignment(self) -> expression:
        exp = self._or()
        
        if self.match(token_type.EQUAL):
            equals : token = self.prev()
            value : expression = self._assignment()
            
            if isinstance(exp, var_exp):
                name : token = exp.name
                return assign_exp(name, value)
            
            self._error(equals, "Invalid assignment target.")
        
        return exp
    
    def _or(self) -> expression:
        exp = self._and()
        
        while self.match(token_type.OR):
            op : token = self.prev()
            right : expression = self._and()
            exp = logical_exp(exp, right, op)
        
        return exp
    
    def _and(self) -> expression:
        exp = self._equality()
        
        while self.match(token_type.AND):
            op : token = self.prev()
            right : expression = self._equality()
            exp = logical_exp(exp, right, op)
        
        return exp
    
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
        
        return self._call()
    
    def _finish_call(self, callee : expression) -> expression:
        args = []
        # if we don't see the ')' in the next token, we have arguments
        if not self.check(token_type.RIGHT_PAREN):
            args.append(self._expression())
            
            # if we see a comma, we have more arguments
            while self.match(token_type.COMMA):
                if len(args) >= 255:
                    self._error(self.peek(), "Cannot have more than 255 arguments.")
                
                args.append(self._expression())
        
        paren = self.consume(token_type.RIGHT_PAREN, "Expect ')' after arguments.")
        
        return call_exp(callee, paren, args)
        
    def _call(self) -> expression:
        exp = self._primary()
        
        while True:
            if self.match(token_type.LEFT_PAREN):
                exp = self._finish_call(exp)
            elif self.match(token_type.DOT):
                name = self.consume(token_type.IDENTIFIER, "Expect property name after '.'.")
                exp = get_exp(exp, name)
            else:
                break
        
        return exp
    
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
        
        if self.match(token_type.IDENTIFIER):
            return var_exp(self.prev())
        
        raise self._error(self.peek(), "Expect expression.")
    
    #endregion
    
    #region other methods
    
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
        
    def declaration(self) -> Optional[statement]:
        try:
            if self.match(token_type.CLASS):
                pass
            if self.match(token_type.FUN):
                pass
            if self.match(token_type.VAR):
                return self._var_declaration()
            
            return None
        except parse_error:
            self.synchronize()
            return None
            
    
    #endregion    
    
    def parse(self) -> List[statement]:
        statements : List[statement] = []
        
        while not self.is_at_end():
            if decl := self.declaration():
                statements.append(decl)
        
        return statements
        