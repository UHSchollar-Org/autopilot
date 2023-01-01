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
        #map1.draw_map()
        #endregion
        
        #region Test2 : Testing add car and pilot to map
        pilot1 = pilot(None)
        car1 = car(pilot1)
        map1.add_car(car1, map1.streets[3])
        assert map1.streets[3].name == pilot1.location.name, "Adding car test failed"
        #endregion
        
        """#region Test3 : Making routes
        _route = route([map1.streets[3],map1.streets[1],map1.streets[4]])
        if _route.is_valid():
            pilot1.route = _route
            for i in range(5):
                map1.move_car(car1)
            assert map1.streets[4] == pilot1.location, f"Moving car test failed, pilot location = {pilot1.location} and most be {map1.streets[4]}"
        else:
            print('Invalid route')
        #endregion"""
        
        #region Test4 : Testing pilot and Stop Signals
        _route = route([map1.streets[39],map1.streets[40]])
        time  = 0
        if _route.is_valid():
            pilot1.route = _route
            for i in range(4):
                map1.move_car(car1)
                time += 1
            assert map1.streets[40] == pilot1.location, f"Stop signals test failed, pilot location = {pilot1.location} and most be {map1.streets[40]}"
        else:
            print('Invalid route')
        #endregion