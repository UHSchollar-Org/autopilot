from __future__ import annotations
from typing import Any, Dict, Optional
from source.pilot_dsl.lexer.token_ import token
from source.pilot_dsl.errors.error import runtime_error

class scope:
    def __init__(self, enclosing : Optional[scope] = None) -> None:
        self.values : Dict[str, Any] = {}
        self.enclosing = enclosing
    
    def define(self, name : str, value):
        self.values[name] = value
    
    def get(self, name: token) -> Any:
        try:
            return self.values[name.lexeme]
        except KeyError:
            pass
        
        if self.enclosing:
            return self.enclosing.get(name)
        
        raise runtime_error(name, f'Undefined variable \'{name.lexeme}\'.')
    
    def ancestor(self, distance : int) -> scope:
        _scope = self
        
        for i in range(distance):
            _scope = _scope.enclosing
        
        return _scope
    
    def get_at(self, distance : int, name : str) -> Any:
        return self.ancestor(distance).values.get(name)
    
    def assign(self, name : token, value : Any):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        
        if self.enclosing:
            self.enclosing.assign(name, value)
            return
        
        raise runtime_error(name, f'Undefined variable \'{name.lexeme}\'.')
    
    def assign_at(self, distance : int, name : token, value : Any):
        self.ancestor(distance).values[name.lexeme] = value