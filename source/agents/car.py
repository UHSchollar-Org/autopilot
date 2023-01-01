from source.environment.map import *
from source.agents.pilot import pilot
from source.agents.client import client
import configparser

config = configparser.ConfigParser()
config.read('source/agents/car.ini')

class car:
    """
    """
    def __init__(self, _pilot : pilot) -> None:
        """Initialization of the CAR class

        Args:
            _pilot (pilot): Pilot is in charge of driving the car and establishing the route
        """
        self.taximeter = 0
        self.distance_price = float(config['DEFAULT']['DISTANCE_PRICE'])
        self.odometer = 0
        self.pilot = _pilot
        self.busy : bool = False
        
    def move(self) -> None:
        """Move the car according to the route given by the pilot
        """
        distance_driven = self.pilot.drive_next_loc()
        self.odometer += distance_driven
        if self.busy:
            self.taximeter += distance_driven * self.distance_price
        self.busy = self.pilot.client_picked_up
