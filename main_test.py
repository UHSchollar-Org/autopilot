from tests import env_test as et
from source.simulation.simulation import simulation
from source.environment._map import map
from source.agents.pilot import pilot
from source.agents.car import car
from source.ia.heuristics.less_time import less_time
from source.ia.heuristics.euclidean_dist import euclidean_distance
from source.ia.heuristics.more_profits import more_profit
from source.pilot_dsl.pilang import pilang
from source.simulation.data_analysis import nyc_yellow_cabs_analysis
from statsmodels.graphics.gofplots import qqplot
import matplotlib.pyplot as plt
from scipy.stats.distributions import lognorm, norm, expon
from source.tools.reader import map_from_json


_map = map_from_json("Map")
garages = [_map.streets[0], _map.streets[1]]
pilot1 = pilot(_map.distance_street_cost, euclidean_distance(), more_profit(), _map, garages)
car1 = car(1, pilot1)
_map.add_car(car1,garages[0])
sim = simulation(_map, [car1], 1, garages, 500)
results = sim.run()
print(results["client_destination_heat_map"])