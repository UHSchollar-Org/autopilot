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
        self.distance_cost = float(config['DEFAULT']['DISTANCE_COST'])
        self.odometer = 0
        self.pilot = _pilot
        self.busy : bool = False
        # remainig kilometers until the car fully discharges
        self.battery : float = float(config['DEFAULT']['BATTERY'])
    
    def get_distance_payment(self, distance : float) -> float:
        """Get the payment of a distance

        Args:
            distance (float): Distance to calculate the payment

        Returns:
            float: Payment of the distance
        """
        return distance * self.distance_price
    
    def get_distance_cost(self, distance : float) -> float:
        """Get the cost of a distance

        Args:
            distance (float): Distance to calculate the cost

        Returns:
            float: Cost of the distance
        """
        return distance * self.distance_cost
    
    def move(self) -> None:
        """Move the car according to the route given by the pilot
        """
        distance_driven = self.pilot.drive_next_loc()
        self.odometer += distance_driven
        if self.busy:
            self.taximeter += self.get_distance_payment(distance_driven)
        self.busy = self.pilot.client_picked_up
