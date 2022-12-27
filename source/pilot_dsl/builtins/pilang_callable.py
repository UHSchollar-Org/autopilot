from abc import ABC, abstractmethod
from typing import List, Any

class pilang_callable(ABC):
    
    @abstractmethod
    def call(self, interpreter, arguments : List[Any]):
        raise NotImplementedError
        
    
    @abstractmethod
    def arity(self) -> int:
        raise NotImplementedError