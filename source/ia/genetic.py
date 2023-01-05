from numpy.random import randint, random
from source.agents.car import car
from source.agents.pilot import pilot
from source.simulation.simulation import simulation
from source.tools.reader import map_from_json
from typing import Dict, Any, List, Tuple

BASE_DATA = {
    "map": map_from_json("Map"),
    "route_selection": [()],
    "client_selection": [],
    "garages": [],
}

class genetic_algorithm:
    def __init__(self, simulations_steps, individuals_c, mutation_rate, generations_c, sim_data = BASE_DATA) -> None:
        self.simulations_steps: int = simulations_steps
        self.sim_data: Dict[str, Any] = sim_data
        self.individuals_c: int = individuals_c
        self.mutation_rate: float = mutation_rate
        self.generations_c: int = generations_c
    
    def generate_cars(self, count) -> List[car]:
        cars: List[car] = []
        route_selection: List[tuple] = self.sim_data["route_selection"]
        client_selection: List = self.sim_data["client_selection"]
        map = self.sim_data["map"]
        garages = self.sim_data["garages"]
        
        for i in range(count):
            r1 = randint(len(route_selection))
            r2 = randint(len(client_selection))
            _pilot = pilot(route_selection[r1][0], route_selection[r1][1], client_selection[r2], map, garages)
            cars.append(car(i+1, _pilot))

        return cars
    
    def create_individual(self) -> simulation:
        _cars_count = randint(500)
        _cars = self.generate_cars(_cars_count)
        
        return simulation(self.sim_data["map"], _cars, _cars_count, self.sim_data["garages"], self.simulations_steps)
    
    def create_population(self) -> List[simulation]:
        population: List[simulation] = []
        
        for _ in range(self.individuals_c):
            population.append(self.create_individual())
            
        return population
    
    def fitness(self, individual: simulation) -> float:
        pass
    
    def selection(self, population: List[simulation]) -> List[simulation]:
        selection = [(individual, self.fitness(individual)) for individual in population]
        selection = [individual for individual in sorted(selection, key=lambda x: x[1], reverse=True)]
        selection = selection[:self.individuals_c//2]
        return selection
    
    def merge_cars(self, cars1: List[car], cars2: List[car], cars_count: int) -> List[car]:
        cars: List[car] = []
        
        for i in range(cars_count):
            if i%2 == 0:
                cars.append(cars1[i])
            else:
                cars.append(cars2[i])
                
            cars[i].id = i+1
        
        return cars
    
    def merge(self, individual1: simulation, individual2: simulation) -> simulation:
        cars_count = individual1.cars_count
        cars = self.merge_cars(individual1.cars, individual2.cars, cars_count)
        
        return simulation(self.sim_data["map"], cars, cars_count, self.sim_data["garages"], self.simulations_steps)
    
    def crossover(self, selection) -> List[simulation]:
        new_population: List[simulation] = []
        
        for i in range(len(selection)//2):
            new_population.append(self.merge(selection[i], selection[len(selection)-i-1]))
        
        for i in range(0, len(selection) - 1, 2):
            new_population.append(self.merge(selection[i], selection[i+1]))
        
        new_population = new_population + selection
              
        return new_population
    
    def extend_cars(self, cars: List[car], cars_count: int) -> List[car]:
        if len(cars) < cars_count:
            cars = cars + self.generate_cars(cars_count - len(cars))
        
        elif len(cars) > cars_count:
            cars = cars[:cars_count]
        
        return cars
        
        
    def mutate(self, individual: simulation) -> simulation:
        if random() < self.mutation_rate:
            cars_count = individual.cars_count + randint(-100, 101)
            cars_count = 1 if cars_count < 1 else cars_count
            
            individual = simulation(individual.map, self.extend_cars(individual.cars, cars_count), cars_count, individual.garages, self.simulations_steps)
        
        return individual
    
    def mutation(self, population) -> List[simulation]:
        for i in range(len(population)):
            population[i] = self.mutate(population[i])
        
        return population
    
    def breed(self, population, selection) -> List[simulation]:
        population = self.crossover(population, selection)
        population = self.mutation(population)
        return population
    
    def run(self) -> List[simulation]:
        population = self.create_population()
        
        for _ in range(self.generations_c):
            selection = self.selection(population)
            population = self.breed(selection)
        
        return population