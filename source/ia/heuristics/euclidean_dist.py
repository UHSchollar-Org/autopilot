from source.ia.heuristics.heuristic import heuristic
from source.tools.general_tools import distance_from_geo_coord

class euclidean_distance(heuristic):
    def evaluate(self, start, end):
        return distance_from_geo_coord(start.geo_coord[0], start.geo_coord[1], end.geo_coord[0], end.geo_coord[1])