from tests import env_test as et
from source.simulation.simulation import simulation
from source.environment._map import map
from source.agents.pilot import pilot
from source.agents.car import car
from source.ia.heuristics.less_time import less_time
from source.ia.heuristics.euclidean_dist import euclidean_distance
from source.tools.reader import map_from_json
from source.ia.heuristics.more_profits import more_profit
from source.tools.general_tools import *

"""a = et.env_test()
a.run_test()"""

_map = map_from_json("Map")

garages = get_garages_loc(_map, 2)

for garage in garages:
    print(garage)