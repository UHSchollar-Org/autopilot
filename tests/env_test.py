from source.environment._map import *
from source.environment.console_printer import print_signs, print_streets, print_street_len
from source.agents.car import *
import source.tools.reader as rd
import networkx as nx
from tests import generic_test

map1 = rd.map_from_json("Vedado")
map1.draw_map()


"""print_signs(map1)
print_streets(map1)
print_street_len(map1)"""

"""class env_test(generic_test):
    
    def run_test(self):
        map1 = rd.map_from_json('Vedado')"""
        