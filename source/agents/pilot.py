from source.environment._map import *

class pilot:
    
    def __init__(self, strategy) -> None:
        self.location : street = None
        self.strategy = strategy
        self.route : route = None
    
    def drive_next_loc(self):
        try:
            next_loc = self.route.peek()
            #Aqui se chequea si es posible moverse hacia la proxima calle
        
            self.location = next(self.route)
        except:
            self.route = None
    
    def load_route(self, _route):
        if _route.peek() != self.location:
            raise Exception('Pilot cannot load a route that does not start at its location')
        else:
            self.route = _route