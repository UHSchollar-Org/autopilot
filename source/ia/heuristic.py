from abc import ABC, abstractmethod
from source.tools.general_tools import distance_from_geo_coord

class heuristic(ABC):
    @abstractmethod
    def evaluate(self, *params):
        raise NotImplementedError

class euclidean(heuristic):
    def evaluate(self, start, end):
        return distance_from_geo_coord(start.geo_coord, end.geo_coord)