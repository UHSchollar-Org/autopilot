from source.ia.heuristics.heuristic import heuristic
from source.ia.heuristics.euclidean_dist import euclidean_distance
from source.ia.astar import astar 
from source.agents.client import client
from source.agents.car import car
from typing import List
from source.environment._map import map, route, intersection
from source.tools.general_tools import from_intersections_to_streets
from source.agents.agency import agency


class more_profit(heuristic):
    def __init__(self, clients : List[client], map : map, car : car, agency : agency, astar : astar) -> None:
        self.clients = clients
        self.map = map
        self.car = car
        self.agency = agency
        self.astar = astar
    
    def get_payment(self, start : intersection, end : intersection) -> float:
        path = self.astar.get_path(start, end)
        return self.agency.get_payment(path)
    
    def get_cost(self, start : intersection, end : intersection) -> float:
        path = self.astar.get_path(start, end)
        return self.agency.get_cost(path)
        
    def evaluate(self):
        client = None
        index = 0
        current_profit = 0
        
        for i, c in enumerate(self.clients):
            cost_to_c = self.get_cost(self.car.pilot.location.intersection2, c.location.intersection2)
            cost_to_dest = self.get_cost(c.location.intersection2, c.destination.intersection2)
            payment = self.get_payment(c.location.intersection2, c.destination.intersection2)
            
            profit = payment - cost_to_c - cost_to_dest
            
            if profit > current_profit:
                current_profit = profit
                index = i
                client = c
        
        return index, client
            
            
            
            