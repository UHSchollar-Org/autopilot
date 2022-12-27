from __future__ import annotations
from .interpreter import scope
from .interpreter import pilang_callable
from source.pilot_dsl.ast.statements import function_stmt
from typing import List, Any

class pilang_func(pilang_callable):
    def __init__(self, declaration : function_stmt, closure : scope, is_init : bool) -> None:
        super().__init__()
        self.closure = closure
        self.declaration = declaration
        self.is_init = is_init
    
    def call(self, interpreter, arguments: List[Any]):
        _scope = scope(self.closure)
        
    def arity(self) -> int:
        return len(self.declaration.params)
    
    def __str__(self) -> str:
        return f'<fn {self.declaration.name.lexeme}>'