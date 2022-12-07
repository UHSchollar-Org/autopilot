from source.environment.map import *
from source.environment.console_printer import print_signs, print_streets, print_street_len
from source.car.car import *
import source.tools.reader as rd
import networkx as nx

map1 = rd.map_from_json("Vedado")
"""
map1.add_street("Paseo", 100, [], (intersection(["Paseo","21"]), intersection(["Paseo","23"])))
map1.add_street("Paseo", 100, [], (intersection(["Paseo","23"]), intersection(["Paseo","21"])))
map1.add_street("Paseo", 100, [], (intersection(["Paseo","23"]), intersection(["Paseo","25"])))
map1.add_street("Paseo", 100, [], (intersection(["Paseo","25"]), intersection(["Paseo","23"])))

map1.add_street("21", 100, [], (intersection(["Paseo","21"]), intersection(["A","21"])))
map1.add_street("21", 100, [], (intersection(["A","21"]), intersection(["B","21"])))
map1.add_street("21", 100, [], (intersection(["B","21"]), intersection(["C","21"])))
map1.add_street("21", 100, [], (intersection(["C","21"]), intersection(["D","21"])))
map1.add_street("21", 100, [], (intersection(["D","21"]), intersection(["E","21"])))
map1.add_street("21", 100, [], (intersection(["E","21"]), intersection(["F","21"])))
map1.add_street("21", 100, [], (intersection(["F","21"]), intersection(["G","21"])))

map1.add_street("23", 100, [], (intersection(["Paseo","23"]), intersection(["A","23"])))
map1.add_street("23", 100, [], (intersection(["A","23"]), intersection(["Paseo","23"])))
map1.add_street("23", 100, [], (intersection(["A","23"]), intersection(["B","23"])))
map1.add_street("23", 100, [], (intersection(["B","23"]), intersection(["A","23"])))
map1.add_street("23", 100, [], (intersection(["B","23"]), intersection(["C","23"])))
map1.add_street("23", 100, [], (intersection(["C","23"]), intersection(["B","23"])))
map1.add_street("23", 100, [], (intersection(["C","23"]), intersection(["D","23"])))
map1.add_street("23", 100, [], (intersection(["D","23"]), intersection(["C","23"])))
map1.add_street("23", 100, [], (intersection(["D","23"]), intersection(["E","23"])))
map1.add_street("23", 100, [], (intersection(["E","23"]), intersection(["D","23"])))
map1.add_street("23", 100, [], (intersection(["E","23"]), intersection(["F","23"])))
map1.add_street("23", 100, [], (intersection(["F","23"]), intersection(["E","23"])))
map1.add_street("23", 100, [], (intersection(["F","23"]), intersection(["G","23"])))
map1.add_street("23", 100, [], (intersection(["G","23"]), intersection(["F","23"])))

map1.add_street("25", 100, [], (intersection(["G","25"]), intersection(["F","25"])))
map1.add_street("25", 100, [], (intersection(["F","25"]), intersection(["E","25"])))
map1.add_street("25", 100, [], (intersection(["E","25"]), intersection(["D","25"])))
map1.add_street("25", 100, [], (intersection(["D","25"]), intersection(["C","25"])))
map1.add_street("25", 100, [], (intersection(["C","25"]), intersection(["B","25"])))
map1.add_street("25", 100, [], (intersection(["B","25"]), intersection(["A","25"])))
map1.add_street("25", 100, [], (intersection(["A","25"]), intersection(["Paseo","25"])))

map1.add_street("G", 100, [], (intersection(["G","25"]), intersection(["G","23"])))
map1.add_street("G", 100, [], (intersection(["G","23"]), intersection(["G","25"])))
map1.add_street("G", 100, [], (intersection(["G","23"]), intersection(["G","21"])))
map1.add_street("G", 100, [], (intersection(["G","21"]), intersection(["G","23"])))
map1.add_street("G", 100, [], (intersection(["G","21"]), intersection(["G","19"])))
map1.add_street("G", 100, [], (intersection(["G","19"]), intersection(["G","21"])))

map1.add_street("19", 100, [], (intersection(["G","19"]), intersection(["E","19"])))

map1.add_street("A", 100, [], (intersection(["A","21"]), intersection(["A","23"])))
map1.add_street("A", 100, [], (intersection(["A","23"]), intersection(["A","25"])))

map1.add_street("B", 100, [], (intersection(["B","25"]), intersection(["B","23"])))
map1.add_street("B", 100, [], (intersection(["B","23"]), intersection(["B","21"])))

map1.add_street("C", 100, [], (intersection(["C","21"]), intersection(["C","23"])))
map1.add_street("C", 100, [], (intersection(["C","23"]), intersection(["C","25"])))

map1.add_street("D", 100, [], (intersection(["D","25"]), intersection(["D","23"])))
map1.add_street("D", 100, [], (intersection(["D","23"]), intersection(["D","21"])))

map1.add_street("E", 100, [], (intersection(["E","19"]), intersection(["E","21"])))
map1.add_street("E", 100, [], (intersection(["E","21"]), intersection(["E","23"])))
map1.add_street("E", 100, [], (intersection(["E","23"]), intersection(["E","25"])))

map1.add_street("F", 100, [], (intersection(["F","25"]), intersection(["F","23"])))
map1.add_street("F", 100, [], (intersection(["F","23"]), intersection(["F","21"])))
"""

"""map1.add_street([], (intersection(["Paseo","21"], (23.132352,-82.395261)), intersection(["Paseo","23"], (23.131296, -82.394285))))
map1.add_street([], (intersection(["Paseo","23"]), intersection(["Paseo","21"])))
map1.add_street([], (intersection(["Paseo","23"]), intersection(["Paseo","25"])))
map1.add_street([], (intersection(["Paseo","25"]), intersection(["Paseo","23"])))

map1.add_street([], (intersection(["Paseo","21"]), intersection(["A","21"])))
map1.add_street([], (intersection(["A","21"]), intersection(["B","21"])))
map1.add_street([], (intersection(["B","21"]), intersection(["C","21"])))
map1.add_street([], (intersection(["C","21"]), intersection(["D","21"])))
map1.add_street([], (intersection(["D","21"]), intersection(["E","21"])))
map1.add_street([], (intersection(["E","21"]), intersection(["F","21"])))
map1.add_street([], (intersection(["F","21"]), intersection(["G","21"])))

map1.add_street([], (intersection(["Paseo","23"]), intersection(["A","23"])))
map1.add_street([], (intersection(["A","23"]), intersection(["Paseo","23"])))
map1.add_street([], (intersection(["A","23"]), intersection(["B","23"])))
map1.add_street([], (intersection(["B","23"]), intersection(["A","23"])))
map1.add_street([], (intersection(["B","23"]), intersection(["C","23"])))
map1.add_street([], (intersection(["C","23"]), intersection(["B","23"])))
map1.add_street([], (intersection(["C","23"]), intersection(["D","23"])))
map1.add_street([], (intersection(["D","23"]), intersection(["C","23"])))
map1.add_street([], (intersection(["D","23"]), intersection(["E","23"])))
map1.add_street([], (intersection(["E","23"]), intersection(["D","23"])))
map1.add_street([], (intersection(["E","23"]), intersection(["F","23"])))
map1.add_street([], (intersection(["F","23"]), intersection(["E","23"])))
map1.add_street([], (intersection(["F","23"]), intersection(["G","23"])))
map1.add_street([], (intersection(["G","23"]), intersection(["F","23"])))

map1.add_street([], (intersection(["G","25"]), intersection(["F","25"])))
map1.add_street([], (intersection(["F","25"]), intersection(["E","25"])))
map1.add_street([], (intersection(["E","25"]), intersection(["D","25"])))
map1.add_street([], (intersection(["D","25"]), intersection(["C","25"])))
map1.add_street([], (intersection(["C","25"]), intersection(["B","25"])))
map1.add_street([], (intersection(["B","25"]), intersection(["A","25"])))
map1.add_street([], (intersection(["A","25"]), intersection(["Paseo","25"])))

map1.add_street([], (intersection(["G","25"]), intersection(["G","23"])))
map1.add_street([], (intersection(["G","23"]), intersection(["G","25"])))
map1.add_street([], (intersection(["G","23"]), intersection(["G","21"])))
map1.add_street([], (intersection(["G","21"]), intersection(["G","23"])))
map1.add_street([], (intersection(["G","21"]), intersection(["G","19"])))
map1.add_street([], (intersection(["G","19"]), intersection(["G","21"])))

map1.add_street([], (intersection(["G","19"]), intersection(["E","19"])))

map1.add_street([], (intersection(["A","21"]), intersection(["A","23"])))
map1.add_street([], (intersection(["A","23"]), intersection(["A","25"])))

map1.add_street([], (intersection(["B","25"]), intersection(["B","23"])))
map1.add_street([], (intersection(["B","23"]), intersection(["B","21"])))

map1.add_street([], (intersection(["C","21"]), intersection(["C","23"])))
map1.add_street([], (intersection(["C","23"]), intersection(["C","25"])))

map1.add_street([], (intersection(["D","25"]), intersection(["D","23"])))
map1.add_street([], (intersection(["D","23"]), intersection(["D","21"])))

map1.add_street([], (intersection(["E","19"]), intersection(["E","21"])))
map1.add_street([], (intersection(["E","21"]), intersection(["E","23"])))
map1.add_street([], (intersection(["E","23"]), intersection(["E","25"])))

map1.add_street([], (intersection(["F","25"]), intersection(["F","23"])))
map1.add_street([], (intersection(["F","23"]), intersection(["F","21"])))"""

nx.write_gexf(map1.simple_map, 'map.gexf')

print_signs(map1)
print_streets(map1)
print_street_len(map1)