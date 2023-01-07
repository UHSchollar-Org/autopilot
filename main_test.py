from tests import env_test as et
from source.simulation.simulation import simulation
from source.environment._map import map
from source.agents.pilot import pilot
from source.agents.car import car
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

garages = [map1.streets[0], map1.streets[1], map1.streets[2]]

pilot1 = pilot(map1.time_street_cost, heuristic, client_selector, map1, garages)
pilot2 = pilot(map1.distance_street_cost, heuristic2, client_selector, map1, garages)

car1 = car(1,pilot1)
car2 = car(2, pilot2)
car3 = car(3, pilot1)
car4 = car(1,pilot1)
car5 = car(2, pilot2)
car6 = car(3, pilot1)
car7 = car(1,pilot1)
car8 = car(2, pilot2)
car9 = car(3, pilot1)
car10 = car(10, pilot1)
car11 = car(11, pilot1)


_simulation = simulation(map1, [car1,car2,car3,car4,car5,car6,car7,car8,car9,car10,car11], 11, garages, 500)

_simulation.run()