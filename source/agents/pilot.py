from source.environment._map import *
from source.environment.traffic_signs import *
from source.tools.general_tools import *
from source.ia.astar import *
from source.ia.heuristics.heuristic import *
from source.ia.heuristics.euclidean_dist import *

class pilot:
    
    def __init__(self, cost_function, heuristic : heuristic, client_selection_strategy : heuristic, _map : map, garages : List) -> None:
        self.map = _map
        self.location : street = None
        self.astar = astar(cost_function, heuristic, _map.adj_dict)
        self.client_selection = client_selection_strategy
        self.route : route = None
        self.trafic_signals_checked = False
        self.client : client = None
        self.client_picked_up : bool = False
        self.garages = garages
    
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
    
    def get_garage_route(self, location : street):
        """From the list of available garages, 
        select the closest one and load the route to it.
        """
        nearest_garage : route = None
        for garage in self.garages:
            intersections = self.astar.get_path(location.intersection2, garage.intersection2)
            garage_route = route(self.map.from_intersections_to_streets(intersections))
            if not nearest_garage or nearest_garage.length == garage_route.length:
                nearest_garage = garage_route
        return nearest_garage
            
        
            
    def select_client(self, clients, battery):
        """Select the most profitable client and load the best route to it

        Args:
            clients (List[client]): List of clients to select
        """
        results = self.client_selection.evaluate()
        result = None
        for _client in results:
            if next_route := self.get_client_route(_client, battery): 
                self.load_route(next_route)
                result = client
                break
        if not result:
            self.load_garage_route(self.get_garage_route())
            
        return result
    
    def get_client_route(self, _client : client, battery):
        """_summary_

        Args:
            _client (client): _description_
        """
        to_client_route = route(self.map.from_intersections_to_streets(
            self.astar.get_path(self.location.intersection2, _client.location.intersection2)))
        client_route = route(self.map.from_intersections_to_streets(
            self.astar.get_path(_client.location.intersection2, _client.destination.intersection2)))
        to_garage_route = route(self.map.from_intersections_to_streets(
            self.get_garage_route(_client.destination)))
        
        total_distance = to_client_route.length + client_route.length + to_garage_route.length
        
        if total_distance < battery:
            return to_client_route.append(client_route)