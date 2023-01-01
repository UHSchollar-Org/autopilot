from source.environment._map import map, street, intersection
from source.agents.car import car
from source.agents.client import client
from source.agents.agency import agency
from typing import List, Dict
from scipy.stats import expon
from random import randint

class simulation:
    def __init__(self, map : map, agency : agency, steps : int) -> None:
        self.map = map
        self.agency = agency
        
        self.next_client : client = None
        # List of clients in the sistem
        self.clients : List[client] = []
        # total steps of the simulation
        self.total_time = steps
               
        #region Simulation variables
        
        # simulation time
        self.current_time = 0
        # total clients picked up 
        self.pickups = 0
        # total clients delivered
        self.deliveries = 0
        # total of pickups for each car
        self.cars_pickups : Dict[car, int] = {c : 0 for c in self.agency.cars}
        # total of money for each car
        self.cars_money : Dict[car, float] = {c : 0 for c in self.agency.cars}
        # total of mantainance spent for each car
        self.cars_mantainance : Dict[car, float] = {c : 0 for c in self.agency.cars}
        
        #endregion
    
    def clients_in_movement(self) -> int:
        return self.pickups - self.deliveries

    def get_destination(self, location : int, distance : float) -> street:
        pass
        
    
    def generate_client(self) -> None:
        wait_time = expon.rvs(size = 1)
        location = randint(0, len(self.map.streets) - 1)
        distance = None
        destination = self.get_destination(location, distance)
        destination = randint(0, len(self.map.streets) - 1)
        self.next_client = client(self.map.streets[location], self.map.streets[destination], self.current_time + wait_time)
        
        
        
    def run(self):
        while self.current_time <= self.total_time:
            
            # Generate client if there is none
            if not self.next_client:
                self.generate_client()
            
            # If next client is in the current time, add it to the sistem and generate a new one
            while self.next_client.request_time <= self.current_time:
                self.clients.append(self.next_client)
                self.generate_client()
            
            # Charge routes for each car
            for car in self.agency.cars:
                # If car is free, pick up a client
                if not car.client:
                    if self.clients:
                        car.client = car.pilot.pick_client(self.clients)
                        self.pickups += 1
                        self.cars_pickups[car] += 1
            
            # Move cars
            for car in self.agency.cars:
                self.map.move_car(car)
            
            
    