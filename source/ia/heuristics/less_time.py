from source.ia.heuristics.heuristic import heuristic
from source.environment._map import *
from source.tools.general_tools import distance_from_geo_coord

class less_time(heuristic):
    
    def __init__(self, long_street_len : float):
        """Estimate the time it takes a car to go from one point to another
        """
        self.longest_street = long_street_len
    
    def evaluate(self,start, end):
        return distance_from_geo_coord(start.geo_coord, end.geo_coord)/self.longest_street