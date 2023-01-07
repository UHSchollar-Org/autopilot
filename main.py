from source.ia.genetic import genetic_algorithm
from source.tools.reader import map_from_json
from source.ia.heuristics.less_time import less_time
from source.ia.heuristics.euclidean_dist import euclidean_distance
from source.ia.heuristics.more_profits import more_profit
from source.environment._map import map
from source.tools.general_tools import get_garages_loc

_map = map_from_json("Map")

sim_data = {
            "map" : _map,
            "route_selection": [(_map.time_street_cost, less_time(_map.get_longest_street())), (map.distance_street_cost, euclidean_distance())],
            "client_selection": [more_profit()],
            "garages": 2
}
sim_data['garages'] = get_garages_loc(_map, sim_data['garages'])

def main():
    print(" ")
    print("Please, enter the parameters for execute the genetic algorithm in the next format:")
    print(f"Parameters: simulations_steps, population_size, mutation_rate, algorithm_generations")
    print("=======================================================================================")
    #read parameters from console
    _input = input()
    _input = _input.split(',')

    sim_steps = int(_input[0])
    population_size = int(_input[1])
    mutation_rate = float(_input[2])
    generations = int(_input[3])
    
    #create the genetic algorithm
    gen = genetic_algorithm(sim_steps, population_size, mutation_rate, generations, sim_data)
    
    result = gen.run()
    
    print("Genetic algorithm result: ")
    
    for key in result:
        print(f'Strategy: {key} - Cars using strategy: {result[key]}')
    
    print("Total cars: ", sum(result.values()))

    print("End of the genetic algorithm")
    print("=======================================================================================")

if __name__ == '__main__':
    main()