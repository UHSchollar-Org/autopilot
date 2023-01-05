from tests import env_test as et
from source.simulation.simulation import simulation
from source.environment._map import map
from source.agents.pilot import pilot
from source.agents.car import car
from source.agents.agency import agency
from source.ia.heuristics.less_time import less_time
from source.ia.heuristics.euclidean_dist import euclidean_distance
import source.tools.reader as rd
from source.ia.heuristics.more_profits import more_profit

"""a = et.env_test()
a.run_test()"""


map1 = rd.map_from_json('Vedado')
heuristic = less_time(map1)
heuristic2 = euclidean_distance()
client_selector = more_profit()
garages = [map1.streets[0]]
pilot1 = pilot(map1.time_street_cost, heuristic, client_selector, map1, garages)
pilot2 = pilot(map1.distance_street_cost, heuristic2, client_selector, map1, garages)
car1 = car(1,pilot1)
car2 = car(2, pilot2)
map1.add_car(car1,map1.streets[0])
map1.add_car(car2, map1.streets[0])
agency1 = agency([car2, car1],[map1.streets[0]])
_simulation = simulation(map1,agency1, 500)

_simulation.run()