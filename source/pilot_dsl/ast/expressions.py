from __future__ import annotations
from abc import ABC, abstractmethod
from source.pilot_dsl.lexer.token_ import token

class exp_visitor(ABC):
    pass

class expression(ABC):
    
    @abstractmethod
    def accept(self, visit):
        raise NotImplementedError

class unary_exp(expression):
    pass

class binary_exp(expression):
    def __init__(self, left_exp : expression, right_exp : expression, operator : token) -> None:
        
        self.left_exp = left_exp
        self.right_exp = right_exp
        self.operator = operator
    
class father_exp(expression):
    pass

class assign_exp(expression):
    pass

class call_exp(expression):
    pass

class get_exp(expression):
    pass

class grouping_exp(expression):
    pass

class literal_exp(expression):
    pass

class logical_exp(expression):
    pass

class set_exp(expression):
    pass

class this_exp(expression):
    pass

class var_exp(expression):
    pass