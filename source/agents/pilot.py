from source.environment._map import *
class pilot:
    
    def __init__(self, strategy) -> None:
        self.location : street = None
        self.strategy = strategy
        self.route : route = None
        