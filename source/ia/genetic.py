from numpy.random import randint, random
from source.agents.car import car
from source.agents.pilot import pilot
from source.simulation.simulation import simulation
from source.tools.reader import map_from_json
from typing import Dict, Any, List
from statistics import median
from copy import deepcopy

BASE_DATA = {
    "map": map_from_json,
    "route_selection": [()],
    "client_selection": [],
    "garages": [],
}

class genetic_algorithm:
    def __init__(self, simulations_steps, population_c, mutation_rate, generations_c, sim_data = BASE_DATA) -> None:
        self.simulations_steps: int = simulations_steps
        self.sim_data: Dict[str, Any] = sim_data
        self.individuals_c: int = population_c
        self.mutation_rate: float = mutation_rate
        self.generations_c: int = generations_c
    
    def generate_cars(self, count, map) -> List[car]:
        cars: List[car] = []
        route_selection: List[tuple] = self.sim_data["route_selection"]
        client_selection: List = self.sim_data["client_selection"]
        garages = simulation.clone_garages(map, self.sim_data["garages"])
        
        for i in range(count):
            r1 = randint(len(route_selection))
            r2 = randint(len(client_selection))
            _pilot = pilot(route_selection[r1][0], route_selection[r1][1], client_selection[r2], map, garages)
            cars.append(car(i+1, _pilot))

        return cars
    
    def create_individual(self) -> simulation:
        _cars_count = randint(1,500)
        new_map = deepcopy(self.sim_data["map"])
        _cars = self.generate_cars(_cars_count, new_map)
        
        return simulation(new_map, _cars, _cars_count, self.sim_data["garages"], self.simulations_steps)
    
    def create_population(self) -> List[simulation]:
        population: List[simulation] = []
        
        for _ in range(self.individuals_c):
            population.append(self.create_individual())
            
        return population
    
    def fitness(self, individual: simulation) -> float:
        
        total_pickups = []
        total_earnings = []
        total_manteinance_cost = []
        
        for _ in range(30):
            individual.reset()
            simulation_results = individual.run()
            
            total_pickups.append(sum(value for value in simulation_results["cars_pickups"].values()))
            total_earnings.append(sum(value for value in simulation_results["cars_money"].values()))
            total_manteinance_cost.append(sum(value for value in simulation_results["cars_manteinance"].values()))
            
        
        total_pickups = median(total_pickups)
        total_earnings = median(total_earnings)
        total_manteinance_cost = median(total_manteinance_cost)
        
        fitness = total_pickups + total_earnings - total_manteinance_cost
        
        fitness -= sum(1 for value in simulation_results["cars_pickups"].values() if value == 0)
        
        return fitness
            
            
    def selection(self, population: List[simulation]) -> List[simulation]:
        selection = [(individual, self.fitness(individual)) for individual in population]
        selection = [individual for individual in sorted(selection, key=lambda x: x[1], reverse=True)]
        selection = selection[:self.individuals_c//2]
        selection = [individual[0] for individual in selection]
        return selection
    
    def merge_cars(self, cars1: List[car], cars2: List[car], cars_count: int) -> List[car]:
        cars: List[car] = []
        
        for i in range(cars_count):
            if i%2 != 0 and i < len(cars2):
                cars.append(cars2[i])
            else:    
                cars.append(cars1[i])
            
            cars[i].id = i+1
        
        return cars
    
    def merge(self, individual1: simulation, individual2: simulation) -> simulation:
        cars_count = individual1.cars_count
        cars = self.merge_cars(individual1.cars, individual2.cars, cars_count)
        new_map = deepcopy(self.sim_data["map"])
        
        return simulation(new_map, cars, cars_count, self.sim_data["garages"], self.simulations_steps)
    
    def crossover(self, selection) -> List[simulation]:
        new_population: List[simulation] = []
        
        for i in range(len(selection)//2):
            new_population.append(self.merge(selection[i], selection[len(selection)-i-1]))
        
        for i in range(0, len(selection) - 1, 2):
            new_population.append(self.merge(selection[i], selection[i+1]))
        
        new_population = new_population + selection
              
        return new_population
    
    def extend_cars(self, cars: List[car], cars_count: int, map) -> List[car]:
        if len(cars) < cars_count:
            cars = cars + self.generate_cars(cars_count - len(cars), map)
        
        elif len(cars) > cars_count:
            cars = cars[:cars_count]
        
        return cars
        
        
    def mutate(self, individual: simulation) -> simulation:
        if random() < self.mutation_rate:
            cars_count = individual.cars_count + randint(-100, 101)
            cars_count = 1 if cars_count < 1 else cars_count
            
            individual = simulation(individual.map, self.extend_cars(individual.cars, cars_count, individual.map), cars_count, individual.garages, self.simulations_steps)
        
        return individual
    
    def mutation(self, population) -> List[simulation]:
        for i in range(len(population)):
            population[i] = self.mutate(population[i])
        
        return population
    
    def breed(self, selection) -> List[simulation]:
        population = self.crossover(selection)
        population = self.mutation(population)
        return population
    
    def analyze_individual(self, individual: simulation):
        results: Dict[str, int] = {}
        
        for i in range(len(individual.cars)):
            key_name = f'{individual.cars[i].pilot.astar.cost_func.__name__}-{type(individual.cars[i].pilot.astar.h).__name__}-{type(individual.cars[i].pilot.client_selection).__name__}'
            
            results[key_name] = results.get(key_name, 0) + 1
        
        return results
            
    def run(self) -> Dict[str, int]:
        population = self.create_population()
        
        for i in range(self.generations_c):
            selection = self.selection(population)
            population = self.breed(selection)
            
            print(f"Generation {i} done")
            
        population = self.selection(population)
        
        results = self.analyze_individual(population[0])
        return results