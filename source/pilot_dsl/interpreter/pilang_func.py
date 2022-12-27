from __future__ import annotations
from .interpreter import scope
from .interpreter import pilang_callable
from source.pilot_dsl.ast.statements import function_stmt
from typing import List, Any
from source.pilot_dsl.errors.error import return_error
from enum import Enum, auto

class function_type(Enum):
    NONE = auto()
    FUNCTION = auto()
    INITIALIZER = auto()
    METHOD = auto()

class pilang_func(pilang_callable):
    def __init__(self, declaration : function_stmt, closure : scope, is_init : bool) -> None:
        super().__init__()
        self.closure = closure
        self.declaration = declaration
        self.is_init = is_init
    
    def call(self, interpreter, arguments: List[Any]):
        _scope = scope(self.closure)
        
        for decl_token, arg in zip(self.declaration.params, arguments):
            _scope.define(decl_token.lexeme, arg)
        
        try:
            interpreter.exec_block(self.declaration.body, _scope)
        except return_error as ret:
            if self.is_init:
                return self.closure.get_at(0, "this")
            
            return ret.value
        
        if self.is_init:
            return self.closure.get_at(0, "this")
        
    def arity(self) -> int:
        return len(self.declaration.params)
    
    def __str__(self) -> str:
        return f'<fn {self.declaration.name.lexeme}>'