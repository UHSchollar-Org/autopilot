import networkx as nx
from traffic_signs import *
import matplotlib.pyplot as plt
import env_tools as tl

## Añadir en el contructor de interseccion el sort a la lista de calles conectadas
## Hay que hacerlo también luego de añadir una calle, a las intersecciones que toque
class intersection:
    
    def __init__(self, connected_streets) -> None:
        self.connected_streets = connected_streets
        self.name = ""
        
        for i in range(len(connected_streets)-1):
            self.name += (connected_streets[i] + '/')
        self.name += connected_streets[len(connected_streets)-1]
            
    def __eq__(self, other) -> bool:
        return tl.same_items(self.connected_streets, other.connected_streets)
    
    def __hash__(self) -> int:## hay que ver si es mejor calcular el hash cuando se crea el objeto para hacerlo solo una vez
        to_hash = ""
        for s in self.connected_streets:
            to_hash += s
        return hash(to_hash)
    
    def __str__(self) -> str:
        return self.name

""""
class street:    
    def __init__(self, inter1, inter2, name, size, signs) -> None:
        self.inter1 = inter1
        self.inter2 = inter2
        self.name = name
        self.size = size
        self.signs = signs
        

class map:
    def __init__(self) -> None:
        self.intersections = list()
        self.streets = dict()
    
    def add_street(self, street):
        pass
    
    def get_adj_inter(self, inter):
        pass
"""


""" Implementación utilizando networkx"""
class map:
    
    def __init__(self, map_name) -> None:
        self.simple_map = nx.DiGraph(name = map_name)
        
    def add_street(self, st_name, st_len, st_signs, joined_intersections):
        if not self.simple_map.has_edge(*joined_intersections):
            for u  in self.simple_map.nodes:
                if not u.connected_streets.__contains__(st_name):
                    if u == joined_intersections[0]:
                        u.connected_streets.append(st_name)
                        u.name += ("/" + st_name) 
                        break
                    elif u == joined_intersections[1]:
                        u.connected_streets.append(st_name)
                        u.name += ("/" + st_name) 
                        break
                    
            self.simple_map.add_edge(*joined_intersections, name = st_name, length = st_len, signs = st_signs)
    
    def print_street(self):
        names = []
        for u,v,name in map1.simple_map.edges(data= "name"):
            if not names.__contains__(name):
                names.append(name)
        names.sort()
        print(names)
                
    def add_sign_to_street(self, inter1, inter2, sign):
        for u,v,signs in self.simple_map.edges(data= signs):
            if u == inter1 and v == inter2:
                signs.append(sign)
    
    def print_signs(self):
        for n, nbrsdict in self.simple_map.adjacency():
            for nbr, eattr in nbrsdict.items():
                to_print = ""
                to_print += str(n) + " -> " + str(nbr) + " : "
                
                for s in eattr.get("signs"):
                    to_print += (str(s) + ",")
                print(to_print)
                    
    def remove_street(self, street):
        pass
    
    def remove_sign_from_street(self, street, sign):
        pass
    
    
map1 = map("mapa1")

map1.add_street("Paseo", 100, [], (intersection(["Paseo","21"]), intersection(["Paseo","23"])))
map1.add_street("Paseo", 100, [], (intersection(["Paseo","23"]), intersection(["Paseo","21"])))
map1.add_street("Paseo", 100, [], (intersection(["Paseo","23"]), intersection(["Paseo","21"])))
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

#map1.print_signs()
map1.print_street()