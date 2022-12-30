from __future__ import annotations
from abc import ABC, abstractmethod
from source.pilot_dsl.lexer.token_ import token
from .expressions import expression, var_exp
from typing import List, Optional

class stmt_visitor(ABC):
    
    @abstractmethod
    def visit_block_stmt(self, stmt : block_stmt):
        raise NotImplementedError
    
    @abstractmethod
    def visit_class_stmt(self, stmt : class_stmt):
        raise NotImplementedError
    
    @abstractmethod
    def visit_expression_stmt(self, stmt : expression_stmt):
        raise NotImplementedError
    
    @abstractmethod
    def visit_function_stmt(self, stmt : function_stmt):
        raise NotImplementedError
    
    @abstractmethod
    def visit_if_stmt(self, stmt : if_stmt):
        raise NotImplementedError
    
    @abstractmethod
    def visit_print_stmt(self, stmt : print_stmt):
        raise NotImplementedError
    
    @abstractmethod
    def visit_return_stmt(self, stmt : return_stmt):
        raise NotImplementedError
    
    @abstractmethod
    def visit_var_stmt(self, stmt : var_stmt):
        raise NotImplementedError
    
    @abstractmethod
    def visit_while_stmt(self, stmt : while_stmt):
        raise NotImplementedError
    
class statement(ABC):
    @abstractmethod
    def validate(self, visit : stmt_visitor):
        raise NotImplementedError

class block_stmt(statement):
    def __init__(self, statements : List[statement]) -> None:
        self.statements = statements
    
    def validate(self, visit: stmt_visitor):
        return visit.visit_block_stmt(self)

class class_stmt(statement):
    def __init__(self, name : token, father_class : Optional[var_exp], methods : List[function_stmt]) -> None:
        self.name = name
        self.father_class = father_class
        self.methods = methods
    
    def validate(self, visit: stmt_visitor):
        return visit.visit_class_stmt(self)

class expression_stmt(statement):
    def __init__(self, exp : expression) -> None:
        self.expression = exp
    
    def validate(self, visit: stmt_visitor):
        return visit.visit_expression_stmt(self)
    
class function_stmt(statement):
    def __init__(self, name : token, params : List[token], body : List[statement]) -> None:
        self.name = name
        self.params = params
        self.body = body
    
    def validate(self, visit: stmt_visitor):
        return visit.visit_function_stmt(self)

class if_stmt(statement):
    def __init__(self, condition : expression, then_branch : statement, else_branch : Optional[statement]) -> None:
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
    
    def validate(self, visit: stmt_visitor):
        return visit.visit_if_stmt(self)

class print_stmt(statement):
    def __init__(self, exp : expression) -> None:
        self.expression = exp
    
    def validate(self, visit: stmt_visitor):
        return visit.visit_print_stmt(self)

class return_stmt(statement):
    def __init__(self, keyword : token, value : Optional[expression]) -> None:
        self.keyword = keyword
        self.value = value
    
    def validate(self, visit: stmt_visitor):
        return visit.visit_return_stmt(self)

class var_stmt(statement):
    def __init__(self, name : token, init : Optional[expression]) -> None:
        self.name = name
        self.initializer = init
    
    def validate(self, visit: stmt_visitor):
        return visit.visit_var_stmt(self)

class while_stmt(statement):
    def __init__(self, condition : expression, body : statement) -> None:
        self.condition = condition
        self.body = body
    
    def validate(self, visit: stmt_visitor):
        return visit.visit_while_stmt(self)