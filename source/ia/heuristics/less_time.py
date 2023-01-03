from source.ia.heuristics.heuristic import heuristic
from source.environment._map import *
from source.tools.general_tools import distance_from_geo_coord

class less_time(heuristic):
    
    def __init__(self, _map : map):
        """Estimate the time it takes a car to go from one point to another
        """
        self.longest_street = self.get_longest_street(_map)
    
    def evaluate(self,start, end):
        return distance_from_geo_coord(start.geo_coord, end.geo_coord)/self.longest_street
    
    def get_longest_street(self, _map : map):
        result = 0
        for _street in _map.streets:
            if _street.length > result:
                result = _street.length
        return result