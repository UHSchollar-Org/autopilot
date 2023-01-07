from abc import ABC, abstractmethod
from typing import Any

class heuristic(ABC):
    @abstractmethod
    def evaluate(self, *params) -> Any:
        raise NotImplementedError
    
