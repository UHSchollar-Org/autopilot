from source.ia.heuristics.heuristic import heuristic
from source.ia.astar import astar 
from source.agents.client import client
from source.agents.car import car
from typing import List
from source.environment._map import intersection, map


class more_profit(heuristic):
    
    def get_payment(self, start : intersection, end : intersection, astar : astar, car : car) -> float:
        path = astar.get_path(start, end)
        path = map.from_intersections_to_streets(path)
        return car.get_distance_payment(sum(s.length for s in path))
    
    def get_cost(self, start : intersection, end : intersection, astar : astar, car : car) -> float:
        path = astar.get_path(start, end)
        path = map.from_intersections_to_streets(path)
        return car.get_distance_cost(sum(s.length for s in path))
        
    def evaluate(self, clients : List[client],  astar : astar, car : car):
        client = None
        index = 0
        current_profit = 0
        
        for i, c in enumerate(clients):
            cost_to_c = self.get_cost(car.pilot.location.intersection2, c.location.intersection2, astar, car)
            cost_to_dest = self.get_cost(c.location.intersection2, c.destination.intersection2, astar, car)
            payment = self.get_payment(c.location.intersection2, c.destination.intersection2, astar, car)
            
            profit = payment - cost_to_c - cost_to_dest
            
            if profit > current_profit:
                current_profit = profit
                index = i
                client = c
        
        return client, index
            
            
            
            