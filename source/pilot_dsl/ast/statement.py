from __future__ import annotations
from abc import ABC, abstractmethod
from source.pilot_dsl.lexer.token_ import token
from .expressions import expression, var_exp
from typing import List, Optional

class stmt_visitor(ABC):
    
    @abstractmethod
    def visit_block(self, stmt : block_stmt):
        raise NotImplementedError
    
    @abstractmethod
    def visit_class(self, stmt : class_stmt):
        raise NotImplementedError
    
    @abstractmethod
    def visit_expression(self, stmt : expression_stmt):
        raise NotImplementedError
    
    @abstractmethod
    def visit_function(self, stmt : function_stmt):
        raise NotImplementedError
    
    @abstractmethod
    def visit_if(self, stmt : if_stmt):
        raise NotImplementedError
    
    @abstractmethod
    def visit_print(self, stmt : print_stmt):
        raise NotImplementedError
    
    @abstractmethod
    def visit_return(self, stmt : return_stmt):
        raise NotImplementedError
    
    @abstractmethod
    def visit_var(self, stmt : var_stmt):
        raise NotImplementedError
    
    @abstractmethod
    def visit_while(self, stmt : while_stmt):
        raise NotImplementedError
    
class statement(ABC):
    @abstractmethod
    def validate(self, visit : stmt_visitor):
        raise NotImplementedError

class block_stmt(statement):
    def __init__(self, statements : List[statement]) -> None:
        self.statements = statements
    
    def validate(self, visit: stmt_visitor):
        return visit.visit_block(self)

class class_stmt(statement):
    def __init__(self, name : token, father_class : Optional[var_exp], methods : List[function_stmt]) -> None:
        self.name = name
        self.father_class = father_class
        self.methods = methods
    
    def validate(self, visit: stmt_visitor):
        return visit.visit_class(self)

class expression_stmt(statement):
    def __init__(self, exp : expression) -> None:
        self.expression = exp
    
    def validate(self, visit: stmt_visitor):
        return visit.visit_expression(self)
    
class function_stmt(statement):
    def __init__(self, name : token, params : List[token], body : List[statement]) -> None:
        self.name = name
        self.params = params
        self.body = body
    
    def validate(self, visit: stmt_visitor):
        return visit.visit_function(self)

class if_stmt(statement):
    def __init__(self, condition : expression, then_branch : statement, else_branch : Optional[statement]) -> None:
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
    
    def validate(self, visit: stmt_visitor):
        return visit.visit_if(self)

class print_stmt(statement):
    def __init__(self, exp : expression) -> None:
        self.expression = exp
    
    def validate(self, visit: stmt_visitor):
        return visit.visit_print(self)

class return_stmt(statement):
    def __init__(self, keyword : token, value : Optional[expression]) -> None:
        self.keyword = keyword
        self.value = value
    
    def validate(self, visit: stmt_visitor):
        return visit.visit_return(self)

class var_stmt(statement):
    def __init__(self, name : token, init : Optional[expression]) -> None:
        self.name = name
        self.initializer = init
    
    def validate(self, visit: stmt_visitor):
        return visit.visit_var(self)

class while_stmt(statement):
    def __init__(self, condition : expression, body : statement) -> None:
        self.condition = condition
        self.body = body
    
    def validate(self, visit: stmt_visitor):
        return visit.visit_while(self)