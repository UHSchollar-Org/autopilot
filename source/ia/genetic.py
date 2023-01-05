from numpy.random import randint, random
from source.simulation.simulation import simulation
from source.tools.reader import map_from_json
from typing import Dict, Any, List

BASE_DATA = {
    "route_selection": [()],
    "client_selection": [],
    "garages": [],
}

class genetic_algorithm:
    def __init__(self, simulations_steps, individuals_c, mutation_rate, selection_c, generations_c, sim_data = BASE_DATA) -> None:
        self.simulations_steps: int = simulations_steps
        self.sim_data: Dict[str, Any] = sim_data
        self.individuals_c: int = individuals_c
        self.mutation_rate: float = mutation_rate
        self.selection_c: int = selection_c
        self.generations_c: int = generations_c
    
    def create_individual(self) -> simulation:
        return simulation(map_from_json("Map"), [], [], self.simulations_steps)
    
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
        selection = selection[:self.selection_c]
        return selection
        
    def crossover(self, population, selection) -> List[simulation]:
        pass
    
    def mutate(self, individual) -> simulation:
        if random() < self.mutation_rate:
            pass # aqui lo mutamos
        
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
            population = self.breed(population, selection)
        
        return population