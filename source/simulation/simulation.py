from source.environment._map import map, street
from source.tools.general_tools import distance_from_geo_coord
from source.agents.car import car
from source.agents.client import client
from typing import List, Dict
from scipy.stats import expon, lognorm
from random import randint
from copy import deepcopy

import numpy as np

class simulation:
    def __init__(self, map : map, cars : List[car], cars_count: int, garages : List[street], steps : int) -> None:
        self.map = deepcopy(map)
        self.cars_count = cars_count
        self.cars = deepcopy(cars)
        self.garages = self.clone_garages(map, garages)
        self.reset_cars()
        self.reset_streets()
        self.add_cars_to_map()
        
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
        self.cars_pickups : Dict[car, int] = {c : 0 for c in self.cars}
        # total of money for each car
        self.cars_money : Dict[car, float] = {c : 0 for c in self.cars}
        # total of mantainance spent for each car
        self.cars_mantainance : Dict[car, float] = {c : 0 for c in self.cars}
        # total of kilometer traveled for each car
        self.cars_kms : Dict[car, float] = {c : 0 for c in self.cars}
        
        #endregion
    
    @staticmethod
    def clone_garages(map, garages: List[street]) -> List[street]:
        new_garages = []
        for street in map.streets:
            if street in garages:
                new_garages.append(street)
        
        return new_garages
    
    def add_cars_to_map(self):
        cars_per_garage = self.cars_count // len(self.garages)
        
        cars_added = 0
        start_index = 0
        for g,garage in enumerate(self.garages):
            for i in range(start_index, len(self.cars)):
                self.map.add_car(self.cars[i], garage)
                cars_added += 1
                
                if g == len(self.garages) - 1:
                    continue
                
                if cars_added == cars_per_garage:
                    cars_added = 0
                    start_index = i+1
                    break
        
        
        
    def clients_in_movement(self) -> int:
        return self.pickups - self.deliveries

    def get_destination(self, location : street, _distance : float) -> street:
        """Returns a location on the map that is the given distance from the starting location. 
           Euclidean distance is used

        Args:
            location (int): Route origin location
            distance (float): Distance that must exist between the origin and the destination

        Returns:
            street: Location that is at the given distance from the received location
        """
        result = None
        error = np.inf
        
        for _street in self.map.streets:
            distance = distance_from_geo_coord(location.intersection1.geo_coord,_street.intersection1.geo_coord)
            if abs(distance - _distance) < error:
                result = _street
                error = abs(distance - _distance)
        
        return result
    
    def update_vars(self, car, results):
        self.cars_mantainance[car] += results[0]*car.distance_cost
        self.cars_kms[car] += results[0]/1000
        
        if results[2]:
            self.pickups += 1
            self.cars_pickups[car] += 1
        
        if results[3]:
            self.deliveries += 1
            self.cars_money[car] += results[1]
    
    def generate_client(self) -> None:
        wait_time = round(expon.rvs(size = 1)[0])
        location = self.map.streets[randint(0, len(self.map.streets) - 1)]
        distance = lognorm.rvs(1)*1000
        destination = self.get_destination(location, distance)
        self.next_client = client(location, destination, self.current_time + wait_time)
        
    def client_to_system(self):
        while self.next_client.request_time <= self.current_time:
            self.clients.append(self.next_client)
            self.generate_client()
    
    def car_pickup(self, car : car):
        if not car.busy and not car.pilot.charging and self.clients:
            if client := car.pilot.select_client(self.clients, car):
                self.clients.remove(client)
                
    def charge_routes(self):
        for car in self.cars:
            self.car_pickup(car)
    
    def move_cars(self):
        for car in self.cars:
            results = self.map.move_car(car)
            self.update_vars(car, results)
    
    def print_status(self):
        print("Time: ", self.current_time)
        print("Clients in movement: ", self.clients_in_movement())
        print("Pickups: ", self.pickups)
        print("Deliveries: ", self.deliveries)
        print("Cars: ")
        for car in self.cars:
            print("Car ", car, " - Pickups: ", self.cars_pickups[car], " - Money: ", round(self.cars_money[car],3), " - Mantainance: ", round(self.cars_mantainance[car],3), " - Kms: ", round(self.cars_kms[car],3))
            print("Location: ", car.pilot.location)
            print("------------------------------------------------------------")
        print("Next client: ", self.next_client)
        print("======================================================================")

    def reset_streets(self):
        for street in self.map.streets:
            street.cars = []
    
    def reset_cars(self):
        for car in self.cars:
            car.reset()
            car.pilot.map = self.map   
    
    def reset(self):
        self.current_time = 0
        self.pickups = 0
        self.deliveries = 0
        self.cars_pickups = {c : 0 for c in self.cars}
        self.cars_money = {c : 0 for c in self.cars}
        self.cars_mantainance = {c : 0 for c in self.cars}
        self.cars_kms = {c : 0 for c in self.cars}
        self.next_client = None
        self.clients = []
        
        self.reset_streets()
        self.add_cars_to_map()
    
    def run(self):
        while self.current_time <= self.total_time:
            
            # Generate client if there is none
            if not self.next_client:
                self.generate_client()
            # If next client is in the current time, add it to the sistem and generate a new one
            self.client_to_system()
            # Charge routes for each car
            self.charge_routes()
            # Move cars
            self.move_cars()
            # Print simulation status
            #self.print_status()
            
            self.current_time += 1
            
            #self.map.draw_map()
            
        results = {
                    "cars_pickups" : self.cars_pickups, 
                    "cars_money" : self.cars_money, 
                    "cars_manteinance" : self.cars_mantainance}
        
        return results
