from source.ia.heuristics.heuristic import heuristic
from source.environment._map import intersection, map
from collections import deque
from typing import Dict, Deque
from source.tools.general_tools import distance_from_geo_coord

class bfs(heuristic):
    
    def evaluate(self, start : intersection, map : map, min_dist : float) -> Dict[intersection, float]:
        q : Deque[intersection] = [start]
        d : Dict[intersection, float] = {start : 0}
        
        while q:
            current_inter = q.popleft()
            for inter in map.adj_dict[inter]:
                if inter not in d.keys():
                    d[inter] = d[current_inter] + distance_from_geo_coord(current_inter.geo_coord, inter.geo_coord)
                    q.append(inter)
                    if d[inter] >= min_dist:
                        return d
        
        return d