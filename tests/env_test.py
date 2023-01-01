from source.environment._map import *
from source.environment.console_printer import print_signs, print_streets, print_street_len
from source.agents.car import *
from source.agents.client import *
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
        pilot1 = pilot(None, map1)
        car1 = car(pilot1)
        map1.add_car(car1, map1.streets[3])
        assert map1.streets[3].name == pilot1.location.name, "Adding car test failed"
        #endregion
        
        #region Test3 : Making routes
        _route = route([map1.streets[3],map1.streets[1],map1.streets[4]])
        if _route.is_valid():
            pilot1.route = _route
            for i in range(5):
                map1.move_car(car1)
            assert map1.streets[4] == pilot1.location, f"Moving car test failed, pilot location = {pilot1.location} and most be {map1.streets[4]}"
        else:
            print('Invalid route')
        #endregion
        
        #region Test4 : Pilot and Stop Signals
        _route = route([map1.streets[39],map1.streets[40]])
        if _route.is_valid():
            pilot1.route = _route
            for i in range(4):
                map1.move_car(car1)
            assert map1.streets[40] == pilot1.location, f"Stop signals test failed, pilot location = {pilot1.location} and most be {map1.streets[40]}"
        else:
            print('Invalid route')
        #endregion
        
        #region Test5: Car odometer & taximeter
        pilot2 = pilot(None, map1)
        car2 = car(pilot2)
        map1.add_car(car2, map1.streets[4])
        _route = route([map1.streets[39],map1.streets[40]])
        car2.pilot.client = client(map1.streets[39],map1.streets[40],2)
        if _route.is_valid():
            pilot2.route = _route
            for i in range(4):
                map1.move_car(car2)
            assert car2.odometer == 282.3, f"Odometer test failed, odometer = {car2.odometer} and most be {282.3}"
            assert car2.taximeter == 0.22860000000000003, f"Taximeter test failed, odometer = {car2.taximeter} and most be {0.22860000000000003}"
        else:
            print('Invalid route')  
        #endregion
        
        #region Test6: Pick up and drop off clients
        pilot3 = pilot(None, map1)
        car3 = car(pilot3)
        map1.add_car(car3, map1.streets[4])
        _route = route([map1.streets[39],map1.streets[40],map1.streets[31]])
        car3.pilot.client = client(map1.streets[39],map1.streets[40],2)
        if _route.is_valid():
            pilot3.route = _route
            for i in range(6):
                map1.move_car(car3)
            assert car3.taximeter == 0.22860000000000003, f"Pick up and drop off clients test failed, taximeter = {car3.taximeter} and most be {0.22860000000000003}"
        else:
            print('Invalid route')
        #endregion