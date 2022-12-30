from source.environment._map import *
from source.environment.console_printer import print_signs, print_streets, print_street_len
from source.agents.car import *
import source.tools.reader as rd
import networkx as nx
from tests.env_test import *
from tests.generic_test import *


#map1 = rd.map_from_json("Vedado")



"""print_signs(map1)
print_streets(map1)
print_street_len(map1)"""

class env_test(test):
    
    def run_test(self):
        
        #region Test1 : Map construction and drawing
        map1 = rd.map_from_json('Vedado')
        map1.draw_map()
        #endregion
        
        #region Test2 : Testing add car and pilot to map
        pilot1 = pilot(None)
        car1 = car(pilot1)
        map1.add_car(car1, map1.streets[0])
        assert map1.streets[0].name == pilot1.location.name, "Adding car test failed"
        #endregion
        