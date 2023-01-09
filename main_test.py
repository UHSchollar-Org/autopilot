from tests import env_test as et
from source.simulation.simulation import simulation
from source.environment._map import map
from source.agents.pilot import pilot
from source.agents.car import car
from source.ia.heuristics.less_time import less_time
from source.ia.heuristics.euclidean_dist import euclidean_distance
from source.pilot_dsl.pilang import pilang

a = pilang()
a.run_file('scas.txt')