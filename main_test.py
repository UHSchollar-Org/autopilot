from tests import env_test as et
from source.simulation.simulation import simulation
from source.environment._map import map
from source.agents.pilot import pilot
from source.agents.car import car
from source.ia.heuristics.less_time import less_time
from source.ia.heuristics.euclidean_dist import euclidean_distance
from source.pilot_dsl.pilang import pilang
from source.simulation.data_analysis import nyc_yellow_cabs_analysis
from statsmodels.graphics.gofplots import qqplot
import matplotlib.pyplot as plt
from scipy.stats.distributions import lognorm, norm, expon

a = nyc_yellow_cabs_analysis()
qqplot(a, dist=expon)
plt.show()