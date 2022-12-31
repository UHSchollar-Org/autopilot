from source.environment._map import *

class pilot:
    
    def __init__(self, strategy) -> None:
        self.location : street = None
        self.strategy = strategy
        self.route : route = None
        self.wait_time = 0
    
    def drive_next_loc(self):
        """The pilot checks the traffic signs of the street where he is,
           then if any sign does not prevent him, he moves to the next 
           street on the route
        """
        if self.wait_time == 0:
            try:
                next_loc = self.route.peek()
                for _signal in self.location.traffic_signs:
                    if isinstance(_signal, stop):
                        return
                self.location = next(self.route)
            except:
                self.route = None
        else:
            self.wait_time -= 1

    def load_route(self, _route):
        if _route.peek() != self.location:
            raise Exception('Pilot cannot load a route that does not start at its location')
        else:
            self.route = _route