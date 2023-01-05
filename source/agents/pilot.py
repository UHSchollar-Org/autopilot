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
    
    def drive_next_loc(self) -> list:
        """The pilot checks the traffic signs and if allowed, 
        moves to the next location on the route. If the route is empty,
        it remains in its location.

        Returns:
            list: Distance_driven, if client was picked up, if client was dropped off
        """
        
        try:
            next_loc = self.route.peek()
            if not self.trafic_signals_checked:
                self.trafic_signals_checked = True
                for _signal in self.location.traffic_signs:
                    if isinstance(_signal, stop):
                        return [0, False, False]
                    
            driven_distance = self.location.length
            self.location = self.map.streets[self.map.streets.index(next(self.route))]
            self.trafic_signals_checked = False
            #If the taxi is at the client's location then it picks them up
            if self.client and self.location == self.client.location:
                self.client_picked_up = True
                return [driven_distance, True, False]
                
            #If the taxi is at the client's destination location then it leaves it
            if self.client_picked_up and self.location == self.client.destination:
                self.client_picked_up = False
                self.client = None
                return [driven_distance, False, True]
            
            #As the taxi is on a new street so it haven't checked the signs for this location
            self.trafic_signals_checked = False
            
            return [driven_distance, False, False]
        except:
            self.route = None
            return [0, False, False]

    def load_route(self, _route):
        if _route.peek().intersection1 != self.location.intersection2:
            raise Exception('Pilot cannot load a route that does not start at its location')
        else:
            self.route = _route
    
    def get_garage_route(self, location):
        from source.environment._map import route
        """From the list of available garages, 
        select the closest one and load the route to it.
        """
        nearest_garage : route = None
        for garage in self.garages:
            intersections = self.astar.get_path(location.intersection2, garage.intersection1)
            garage_route = route(self.map.from_intersections_to_streets(intersections)).append(route([garage]))
            
            if not nearest_garage or nearest_garage.length == garage_route.length:
                nearest_garage = garage_route
        return nearest_garage
            
        
            
    def select_client(self, clients, car):
        """Select the most profitable client and load the best route to it

        Args:
            clients (List[client]): List of clients to select
        """
        results = self.client_selection.evaluate(clients, self.astar, car)
        result = None
        for _client in results:
            _client = _client[0]
            if next_route := self.get_client_route(_client, car.battery): 
                self.load_route(next_route)
                result = _client
                self.client = _client
                break
        if not result:
            self.load_route(self.get_garage_route(car.pilot.location))
            
        return result
    
    def get_client_route(self, _client, battery):
        from source.environment._map import route
        """_summary_

        Args:
            _client (client): _description_
        """
        to_client_route = route(self.map.from_intersections_to_streets(
            self.astar.get_path(self.location.intersection2, _client.location.intersection1)))
        
        to_client_route = to_client_route.append(route([_client.location]))
        
        client_route = route(self.map.from_intersections_to_streets(
            self.astar.get_path(_client.location.intersection2, _client.destination.intersection1)))

        client_route = client_route.append(route([_client.destination]))
        
        to_garage_route = self.get_garage_route(_client.destination)
        
        total_distance = to_client_route.length + client_route.length + to_garage_route.length
        
        if total_distance < battery:
            return to_client_route.append(client_route)