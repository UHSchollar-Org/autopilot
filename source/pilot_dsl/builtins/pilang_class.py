from __future__ import annotations
from enum import Enum, auto
from .pilang_callable import pilang_callable
from .pilang_func import pilang_func
from typing import Any, List, Dict, Optional


class class_type(Enum):
    NONE = auto()
    CLASS = auto()
    SUBCLASS = auto()
    
class pilang_class(pilang_callable):
    def __init__(self, name : str, father_class : Optional[pilang_class], methods : Dict[str, pilang_func]) -> None:
        self.name = name
        self.father_class = father_class
        self.methods = methods
    
    def call(self, interpreter, arguments: List[Any]):
        return super().call(interpreter, arguments)
    
    def arity(self) -> int:
        init = self.find_method("init")
        if init is not None:
            return init.arity()
        else:
            return 0
    
    def __repr__(self) -> str:
        return self.name
    
    def find_method(self, name : str) -> Optional[pilang_func]:
        pass
    
    def __str__(self) -> str:
        return f'<class {self.name}>'