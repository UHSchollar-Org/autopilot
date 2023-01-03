from source.ia.heuristics.heuristic import heuristic
from source.ia.heuristics.euclidean_dist import euclidean_distance
from source.ia.astar import astar 
from source.agents.client import client
from source.agents.car import car
from typing import Dict
from source.environment._map import map, route, intersection
from source.tools.general_tools import from_intersections_to_streets
from source.agents.agency import agency


class more_profit(heuristic):
    @staticmethod
    def evaluate(self, clients : Dict[client, route], map : map, car : car, agency : agency):
        _astar : astar = astar(intersection.distance, euclidean_distance, map.adj_dict)
        client = clients[0]
        cost_to_c = 0
        cost_to_dest = 0
        
        for c in clients[1:]:
            path_to_c = _astar.get_path(car.pilot.location.intersection2, c.location.intersection2)
            client_to_dest = _astar.get_path(c.location.intersection2, c.destination.intersection2)
            path_to_c = from_intersections_to_streets(path_to_c)
            client_to_dest = from_intersections_to_streets(client_to_dest)
            
            cost_to_c = agency.get_cost(path_to_c)
            cost_to_dest = agency.get_cost(client_to_dest)
            payment = agency.get_payment(client_to_dest)
            
            
            
            
            