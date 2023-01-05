from numpy.random import randint
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
        """_summary_
        """
        
        
        sim = simulation(map_from_json("Map"), [], [], self.simulations_steps)
    
    def create_population(self) -> List[simulation]:
        population: List[simulation] = []
        
        for _ in range(self.individuals_c):
            population.append(self.create_individual())
            
        return population
    
    def fitness(self, individual: simulation) -> float:
        pass
    
    def selection(self, population: List[simulation]) -> List[simulation]:
        new_population: List[simulation] = []
        
        
    
    def crossover(self):
        pass
    
    def mutation(self):
        pass
    
    def breed(self):
        pass
    
    def evolve(self):
        pass
    
    def run(self):
        pass
    