from __future__ import annotations
from abc import ABC, abstractmethod
from source.pilot_dsl.lexer.token_ import token
from typing import List

class exp_visitor(ABC):
    
    @abstractmethod
    def visit_unary(self, exp : unary_exp):
        raise NotImplementedError
    
    @abstractmethod
    def visit_binary(self, exp : binary_exp):
        raise NotImplementedError
    
    @abstractmethod
    def visit_father(self, exp : father_exp):
        raise NotImplementedError
    
    @abstractmethod
    def visit_assign(self, exp : assign_exp):
        raise NotImplementedError
    
    @abstractmethod
    def visit_call(self, exp : call_exp):
        raise NotImplementedError
    
    @abstractmethod
    def visit_get(self, exp : get_exp):
        raise NotImplementedError
    
    @abstractmethod
    def visit_grouping(self, exp : grouping_exp):
        raise NotImplementedError
    
    @abstractmethod
    def visit_literal(self, exp : literal_exp):
        raise NotImplementedError
    
    @abstractmethod
    def visit_logical(self, exp : logical_exp):
        raise NotImplementedError
    
    @abstractmethod
    def visit_set(self, exp : set_exp):
        raise NotImplementedError
    
    @abstractmethod
    def visit_this(self, exp : this_exp):
        raise NotImplementedError
    
    @abstractmethod
    def visit_var(self, exp : var_exp):
        raise NotImplementedError

class expression(ABC):
    
    @abstractmethod
    def validate(self, visit : exp_visitor):
        raise NotImplementedError

class unary_exp(expression):
    def __init__(self, operator : token, exp : expression) -> None:
        self.operator = operator
        self.exp = exp
    
    def validate(self, visit: exp_visitor):
        return visit.visit_unary(self)

class binary_exp(expression):
    def __init__(self, left_exp : expression, right_exp : expression, operator : token) -> None:
        
        self.left_exp = left_exp
        self.right_exp = right_exp
        self.operator = operator
    
    def validate(self, visit: exp_visitor):
        return visit.visit_binary(self)
    
class father_exp(expression):
    def __init__(self, keyword : token, method : token) -> None:
        self.keyword = keyword
        self.method = method
        
    def validate(self, visit: exp_visitor):
        return visit.visit_father(self)

class assign_exp(expression):
    def __init__(self, name : token, value : expression) -> None:
        self.name = name
        self.value = value
        
    def validate(self, visit: exp_visitor):
        return visit.visit_assign(self)

class call_exp(expression):
    def __init__(self, callee : expression, paren : token, args : List[expression]) -> None:
        self.callee = callee
        self.paren = paren
        self.args = args
    
    def validate(self, visit: exp_visitor):
        return visit.visit_call(self)

class get_exp(expression):
    def __init__(self, object : expression, name : token) -> None:
        self.object = object
        self.name = name
    
    def validate(self, visit: exp_visitor):
        return visit.visit_get(self)

class grouping_exp(expression):
    def __init__(self, exp : expression) -> None:
        self.exp = exp
    
    def validate(self, visit: exp_visitor):
        return visit.visit_grouping(self)
    
class literal_exp(expression):
    def __init__(self, value) -> None:
        self.value = value
        
    def validate(self, visit: exp_visitor):
        return visit.visit_literal(self)

class logical_exp(expression):
    def __init__(self, left_exp : expression, right_exp : expression, operator : token) -> None:
        self.left_exp = left_exp
        self.right_exp = right_exp
        self.operator = operator

    def validate(self, visit: exp_visitor):
        return visit.visit_logical(self)
    
class set_exp(expression):
    def __init__(self, object : expression, name : token, value : expression) -> None:
        self.object = object
        self.name = name
        self.value = value
    
    def validate(self, visit: exp_visitor):
        return visit.visit_set(self)

class this_exp(expression):
    def __init__(self, keyword : token) -> None:
        self.keyword = keyword
    
    def validate(self, visit: exp_visitor):
        return visit.visit_this(self)

class var_exp(expression):
    def __init__(self, name : token) -> None:
        self.name = name
    
    def validate(self, visit: exp_visitor):
        return visit.visit_var(self)