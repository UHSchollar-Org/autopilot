from __future__ import annotations
from typing import *
from source.tools.general_tools import *
from source.agents.car import *
from source.environment.traffic_signs import *

import networkx as nx
import matplotlib.pyplot as plt


class intersection:
    
    def __init__(self,connected_streets, geo_coord) -> None:
        self.connected_streets = connected_streets
        self.geo_coord = geo_coord
        self.name = ""
        
        for i in range(len(connected_streets)-1):
            self.name += (connected_streets[i] + '/')
        self.name += connected_streets[len(connected_streets)-1]
    
    @staticmethod
    def distance(inter1 : intersection, inter2 : intersection):
        return distance_from_geo_coord(inter1.geo_coord, inter2.geo_coord)
    
    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)
        
    def __hash__(self) -> int:
        return hash(self.name)
    
    def __str__(self) -> str:
        return self.name

class street:
    
    def __init__(self, intersection1 : intersection, intersection2 : intersection, traffic_signs : List[signal] = []) -> None:
        self.intersection1 = intersection1
        self.intersection2 = intersection2
        self.cars = []
        self.traffic_signs = traffic_signs
        self.length =  distance_from_geo_coord( intersection1.geo_coord, intersection2.geo_coord)
        self.name = self.intersection1.name + " --- " + self.intersection2.name
        
    def add_car(self, _car : car):
        """Add the car to the internal list of cars

        Args:
            _car (car): Car to be addded
        """
        self.cars.append(_car)
        _car.pilot.location = self
    
    def remove_car(self, _car : car):
        """Remove the car to the internal list of cars

        Args:
            _car (car): Car to be removed
        """
        try: 
            self.cars.remove(_car)
        except:
            raise Exception("The car is not in this street")

    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)
        
    def __hash__(self) -> int:
        return hash(self.intersection1.name + self.intersection2.name)
    
    def __str__(self) -> str:
        return self.intersection1.name + " --> " + self.intersection2.name

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
            
        _street = street(inter1,inter2,st_signs)
        if _street not in self.streets:
            self.streets.append(_street)
            self.adj_dict[inter1].append(inter2)
    
    def get_longest_street(self):
        result = 0
        for _street in self.streets:
            if _street.length > result:
                result = _street.length
        return result
    
    def add_car(self, _car : car, location : street):
        """Add the given car to the guiven street

        Args:
            _car (car): Car to be added
            location (street): Street where the car will be added
        """
        try:
            index = self.streets.index(location)
            self.streets[index].add_car(_car)
        except:
            raise Exception("The given street dont belong to the map")
    
    def move_car(self, _car : car):
        """_summary_

        Args:
            _car (car): _description_
        """
        start_loc = _car.pilot.location
        results = _car.move()
        end_loc = _car.pilot.location
        if start_loc != end_loc:
            start_loc.remove_car(_car)
            end_loc.add_car(_car)
        
        return results
    
    def draw_map(self):
        graph = nx.DiGraph()
        pos = {}
        for _street in self.streets:
            pos[_street.intersection1] = _street.intersection1.geo_coord
            pos[_street.intersection2] = _street.intersection2.geo_coord
            graph.add_edge(_street.intersection1,_street.intersection2)
            
        #subax1 = plt.subplot(121)
        nx.draw(graph, pos=pos,  with_labels=True, font_weight='bold')
        
        plt.show()
 
    #region Cost functions
    @staticmethod
    def distance_street_cost(Intersection1: intersection, intersection2: intersection):
        return distance_from_geo_coord(Intersection1.geo_coord, intersection2.geo_coord)
    
    def time_street_cost(self, Intersection1: intersection, intersection2: intersection):
        aux = street(Intersection1,intersection2)
        cost = 1
        traffic_signals = None
        for _street in self.streets:
            if _street==aux:
                traffic_signals = _street.traffic_signs
                break
        
        for traffic_signal in traffic_signals:
            if isinstance(traffic_signal, stop):
                cost += 1
            if isinstance(traffic_signal, traffic_light):
                cost += 2
                
        return cost
    #endregion
    
    @staticmethod
    def from_intersections_to_streets(intersections : List[intersection]) -> List[street]:
        """Dada una lista de intersecciones devuelve la lista de calles que forman
        """
        result : List[street] = []
        for i in range(1,len(intersections)):
            result.append(street(intersections[i-1], intersections[i]))
        return result
    
class route:
    
    def __init__(self, streets : List[street]) -> None:

        self.streets = streets 
        self.length = self.get_route_length()
        self.current = 0
        self.destination : street = streets[-1] if self.streets != [] else None
    
    
    def get_route_length(self) -> float:
        """Calculate the length of the route


        Returns:
            int: Length of the route in meters
        """
        distance_sum = 0
        try:
            for _street in self.streets:
                distance_sum += _street.length
        except:
            pass
        return distance_sum
    
    def is_valid(self) -> bool:
        """Check if a valid route. The street at position i must have 
           an intersection in common with the street at position i+1

        Returns:
            bool: True if this route instance is a valid route
        """
        for i in range(1,len(self.streets)):
            _street = self.streets[i-1]
            next_street = self.streets[i]
            if _street.intersection2 != next_street.intersection1:
                return False
        return True
                
    def __str__(self) -> str:
        result = ''
        for _street in self.streets:
            result += _street.name + '|'
        return result
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current < len(self.streets):
            result = self.streets[self.current]
            self.current += 1
            return result
        else:
            self.current = 0
            raise StopIteration('Iteration is finished')    
    
    def peek(self) -> street:
        """Return the current street on the route

        Returns:
            street: Result of streets[current]
        """
        return self.streets[self.current]
    
    
    def append(self, other_route : route):
        """_summary_

        Args:
            other_route (route): _description_
        """
        streets = self.streets + other_route.streets
        resulting_route = route(streets)
        return resulting_route if resulting_route.is_valid() else None