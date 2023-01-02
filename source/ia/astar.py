from source.environment._map import intersection
from .heuristic import heuristic
from typing import Dict, List
from source.tools.general_tools import distance_from_geo_coord

class astar:
    def __init__(self, h : heuristic, adj_dict : Dict[intersection, List[intersection]]) -> None:
        self.h = h
        self.adj_dict = adj_dict
            
    def get_path(self, start : intersection, end : intersection) -> List[intersection]:
        open_nodes : List[intersection] = [start]
        closed_nodes : List[intersection] = []
        pi : Dict[intersection, intersection] = {start:start}
        distances : Dict[intersection, float] = {start:0}
        
        while open_nodes:
            
            current = None
            for inter in open_nodes:
                if current is None or distances[inter] + self.h.evaluate(inter, end) < distances[current] + self.h.evaluate(current, end):
                    current = inter
            
            if current == end:
                path : List[intersection] = []
                
                while pi[current] != current:
                    path.append(current)
                    current = pi[current]
                
                path.append(current)
                path.reverse()
                
                return path
            
            for adj in self.adj_dict[current]:
                w = distance_from_geo_coord(current.geo_coord, adj.geo_coord)
                
                if adj not in closed_nodes and adj not in open_nodes:
                    open_nodes.append(adj)
                    pi[adj] = current
                    distances[adj] = distances[current] + w
                
                elif distances[adj] > distances[current] + w:
                    pi[adj] = current
                    distances[adj] = distances[current] + w
                    
                    if adj in closed_nodes:
                        closed_nodes.remove(adj)
                        open_nodes.append(adj)
            
            open_nodes.remove(current)
            closed_nodes.append(current)
        
        return []
