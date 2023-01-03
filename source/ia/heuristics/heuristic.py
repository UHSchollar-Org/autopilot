from abc import ABC, abstractmethod
from source.tools.general_tools import distance_from_geo_coord
from typing import Any

class heuristic(ABC):
    @abstractmethod
    @staticmethod
    def evaluate(self, *params) -> Any:
        raise NotImplementedError

    
