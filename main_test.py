from tests import env_test as et
from source.simulation.simulation import simulation
from source.environment._map import map
from source.agents.pilot import pilot
from source.agents.car import car
from source.agents.agency import agency
from source.ia.heuristics.less_time import less_time
import source.tools.reader as rd

"""a = et.env_test()
a.run_test()"""


map1 = rd.map_from_json('Vedado')
heuristic = less_time(map1)
pilot1 = pilot(map1.time_street_cost, heuristic, map1, [map1.streets[0]])
car1 = car(pilot1)
map1.add_car(car1,map1.streets[0])
agency1 = agency([car1],[map1.streets[0]])
_simulation = simulation(map1,agency1, 50)

_simulation.run()