from source.agents.pilot import pilot
from source.agents.client import client
import configparser

config = configparser.ConfigParser()
config.read('source/agents/car.ini')

class car:
    """
    """
    def __init__(self, id : int,  _pilot : pilot) -> None:
        """Initialization of the CAR class

        Args:
            _pilot (pilot): Pilot is in charge of driving the car and establishing the route
        """
        self.id = id
        self.taximeter = 0
        self.distance_price = float(config['DEFAULT']['DISTANCE_PRICE'])
        self.distance_cost = float(config['DEFAULT']['DISTANCE_COST'])
        self.odometer = 0
        self.pilot = _pilot
        self.busy : bool = False
        # remainig kilometers until the car fully discharges
        self.battery_capacity : float = float(config['DEFAULT']['BATTERY'])
        self.battery : float = self.battery_capacity
        self.carge_speed : float = float(config['DEFAULT']['CHARGE_SPEED'])
    
    def reset(self):
        self.taximeter = 0
        self.taximeter = 0
        self.odometer = 0
        self.busy : bool = False
        self.battery : float = float(config['DEFAULT']['BATTERY'])
        self.pilot.client = None
        self.pilot.client_picked_up = False
        self.pilot.location = None
        self.pilot.route = None
    
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
    
    def update_taximeter(self, distance : float) -> None:
        if self.pilot.client_picked_up:
            self.taximeter += self.get_distance_payment(distance)
        
    
    def update_odometer(self, distance : float) -> None:
        self.odometer += distance
    
    def check_busy(self) -> None:
        self.busy = self.pilot.route != None
    
    def update_battery(self, distance : float):
        self.battery -= distance
        if self.pilot.charging:
            new_battery_status = self.battery + self.carge_speed
            self.battery = new_battery_status if new_battery_status <= self.battery_capacity else self.battery_capacity
            if self.battery == self.battery_capacity:
                self.pilot.charging = False
            
    
    def move(self):
        """Move the car according to the route given by the pilot
        """
        results = self.pilot.drive_next_loc()
        distance_driven = results[0]
        picked_up = results[1]
        dropped_off = results[2]
        
        self.update_odometer(distance_driven)
        self.update_taximeter(distance_driven)
        self.check_busy()
        self.update_battery(distance_driven)
        
        ret = [distance_driven, self.taximeter, picked_up, dropped_off]
        
        self.taximeter = 0 if not self.pilot.client_picked_up else self.taximeter
        
        return ret

    def __str__(self) -> str:
        return f'<car {self.id}>'