from source.environment.map import *
from source.environment.console_printer import print_signs, print_streets, print_street_len
from source.car.car import *
import source.tools.reader as rd
import networkx as nx
from tests.generic_test import test

#this is incomplete

map1 = rd.map_from_json("Vedado")

nx.write_gexf(map1.simple_map, 'map.gexf')

print_signs(map1)
print_streets(map1)
print_street_len(map1)

class env_test(test):
    
    def run_test(self):
        map1 = rd.map_from_json('Vedado')
        