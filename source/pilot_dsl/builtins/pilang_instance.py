from __future__ import annotations
from typing import Any, Dict
from source.pilot_dsl.lexer.token_ import token
from source.pilot_dsl.errors.error import runtime_error

class pilang_instance:
    def __init__(self, _class) -> None:
        self._class = _class
        self.fields : Dict[str, Any] = {}
    
    def __repr__(self) -> str:
        return f'<instance {self._class.name}>'
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def get(self, name : token) -> Any:
        try:
            return self.fields[name.lexeme]
        except KeyError:
            pass
        
        raise runtime_error(name, f'Undefined property \'{name.lexeme}\'')
    
    def set(self, name : token, value : Any):
        self.fields[name.lexeme] = value