from source.agents.car import car
from source.agents.pilot import pilot
from typing import List
from source.agents.garage import garage
from source.environment._map import map

class agency:
    def __init__(self, cars : List[car], garages : List[garage]) -> None:
        self.cars = cars
        self.garages = garages
    