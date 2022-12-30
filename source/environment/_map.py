from typing import *
from source.tools.general_tools import *

class intersection:
    
    def __init__(self,connected_streets, geo_coord) -> None:
        self.connected_streets = connected_streets
        self.geo_coord = geo_coord
        self.name = ""
        
        for i in range(len(connected_streets)-1):
            self.name += (connected_streets[i] + '/')
        self.name += connected_streets[len(connected_streets)-1]
        
    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)
        
    def __hash__(self) -> int:
        return hash(self.name)
    
    def __str__(self) -> str:
        return self.name

class street:
    
    def __init__(self, intersection1 : intersection, intersection2 : intersection) -> None:
        self.intersection1 = intersection1
        self.intersection2 = intersection2
        self.length =  distance_from_geo_coord( intersection1.geo_coord[0], 
                                                intersection1.geo_coord[1],
                                                intersection2.geo_coord[0],
                                                intersection2.geo_coord[1])
        self.name = self.intersection1.name + " --- " + self.intersection2.name


    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)
        
    def __hash__(self) -> int:
        return hash(self.intersection1.name + self.intersection2.name)
    
    def __str__(self) -> str:
        return self.name

class map:
    def __init__(self, name) -> None:
        self.name = name
        self.intersections : List[intersection] = []
        self.streets : List[street] = []
        self.adj_dict : Dict[intersection, List[intersection]] = {}
        
    def add_street(self, st_signs, _intersections):
        inter1, inter2 = _intersections

        if inter1 not in self.intersections:
            self.intersections.append(inter1)
            self.adj_dict[inter1] = []

        if inter2 not in self.intersections:
            self.intersections.append(inter2)
            self.adj_dict[inter2] = []
            
        _street = street(inter1,inter2)
        if _street not in self.streets:
            self.streets.append(_street)
            self.adj_dict[inter1].append(inter2)
            
        
    
class route:
    
    def __init__(self, streets : List[street]) -> None:
        self.streets : List[street] = streets
        self.length = self.get_route_length()
    
    def get_route_length(self) -> float:
        """Calculate the length of the route

        Returns:
            int: Length of the route in meters
        """
        distance_sum = 0
        for _street in self.streets:
            distance_sum += _street.length
        return distance_sum
    
    def __iter__(self):
        return route_iterator(self)
    
class route_iterator:
    
    def __init__(self, rte : route):
        self.rte = rte
        self.current = 0
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current < len(self.rte.route):
            result = self.rte.route[self.current]
            self.current += 1
            return result
        else:
            self.current = 0
            raise StopIteration('Iteration is finished')