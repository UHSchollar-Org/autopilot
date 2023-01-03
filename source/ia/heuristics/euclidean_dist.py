from source.ia.heuristics.heuristic import heuristic
from source.tools.general_tools import distance_from_geo_coord

class euclidean_distance(heuristic):
    
    def evaluate(start, end):
        return distance_from_geo_coord(start.geo_coord, end.geo_coord)