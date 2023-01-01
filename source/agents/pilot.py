from source.environment._map import *
from source.environment.traffic_signs import *
from source.tools.general_tools import *

class pilot:
    
    def __init__(self, strategy) -> None:
        self.location : street = None
        self.strategy = strategy
        self.route : route = None
        self.wait_time = 0
        self.trafic_signals_checked = False
    
    def drive_next_loc(self) -> float:
        """The pilot checks the traffic signs and if allowed, 
        moves to the next location on the route. If the route is empty,
        it remains in its location.

        Returns:
            float: Distance that was driven in meters
        """
        if self.wait_time == 0:
            try:
                next_loc = self.route.peek()
                if not self.trafic_signals_checked:
                    self.trafic_signals_checked = True
                    for _signal in self.location.traffic_signs:
                        if isinstance(_signal, stop):
                            return 0
                driven_distance = self.location.length
                self.location = next(self.route)
                self.trafic_signals_checked = False
                return driven_distance
            except:
                self.route = None
                return 0
        else:
            self.wait_time -= 1

    def load_route(self, _route):
        if _route.peek() != self.location:
            raise Exception('Pilot cannot load a route that does not start at its location')
        else:
            self.route = _route