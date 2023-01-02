from source.environment._map import *
from source.environment.traffic_signs import *
from source.tools.general_tools import *
from source.ia.astar import *
from source.ia.heuristic import *

class pilot:
    
    def __init__(self, strategy, _map : map, garages : List[street]) -> None:
        self.map = _map
        self.location : street = None
        self.strategy = strategy
        self.route : route = None
        self.trafic_signals_checked = False
        self.client : client = None
        self.client_picked_up : bool = False
        self.garages = garages
        self.astar = astar(euclidean,self.map.adj_dict)
    
    def drive_next_loc(self) -> float:
        """The pilot checks the traffic signs and if allowed, 
        moves to the next location on the route. If the route is empty,
        it remains in its location.

        Returns:
            float: Distance that was driven in meters
        """
        try:
            next_loc = self.route.peek()
            if not self.trafic_signals_checked:
                self.trafic_signals_checked = True
                for _signal in self.location.traffic_signs:
                    if isinstance(_signal, stop):
                        return 0
            driven_distance = self.location.length
            self.location = next(self.route)
            #If the taxi is at the client's location then it picks them up
            if self.client and self.location == self.client.location:
                self.client_picked_up = True
                """Aqui calculamos la ruta hacia el destino del cliente"""
                
            #If the taxi is at the client's destination location then it leaves it
            if self.client and self.location == self.client.destination:
                self.client_picked_up = False
                self.client = None
            #As the taxi is on a new street so it haven't checked the signs for this location
            self.trafic_signals_checked = False
            
            return driven_distance
        except:
            self.route = None
            return 0

    def load_route(self, _route):
        if _route.peek() != self.location:
            raise Exception('Pilot cannot load a route that does not start at its location')
        else:
            self.route = _route
    
    def load_garage_route(self):
        """From the list of available garages, 
        select the closest one and load the route to it.
        """
        for garage in self.garages:
            intersections = self.astar.get_path(self.location.intersection1, garage.intersection1)
            self.route = route(from_intersections_to_streets(intersections))    
            
    def select_client(self, clients):
        """Select the most profitable client and load the best route to it

        Args:
            clients (List[client]): List of clients to select
        """
        result = None
        
        if not result:
            self.load_garege_route()