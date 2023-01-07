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

ga = genetic_algorithm(50, 10, 0.2, 5, sim_data)

best_vars = ga.run()

for key in best_vars:
    print(key,' : ', best_vars[key])
