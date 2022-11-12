import networkx as nx
from .traffic_signs import *
import tools.general_tools as tl


## Añadir en el contructor de interseccion el sort a la lista de calles conectadas
## Hay que hacerlo también luego de añadir una calle, a las intersecciones que toque
class intersection:
    
    def __init__(self, connected_streets, geo_coord) -> None:
        self.connected_streets = connected_streets
        self.geo = geo_coord
        self.name = ""
        
        for i in range(len(connected_streets)-1):
            self.name += (connected_streets[i] + '/')
        self.name += connected_streets[len(connected_streets)-1]
            
    def __eq__(self, other) -> bool:
        return tl.same_items(self.connected_streets, other.connected_streets)
    
    ## hay que ver si es mejor calcular el hash cuando se crea el objeto para hacerlo solo una vez
    def __hash__(self) -> int:
        to_hash = ""
        for s in self.connected_streets:
            to_hash += s
        return hash(to_hash)
    
    def __str__(self) -> str:
        return self.name

""" Implementación utilizando networkx"""
class map:
    
    def __init__(self, map_name) -> None:
        self.simple_map = nx.DiGraph(name = map_name)
        
    def add_street(self, st_signs, joined_intersections):
        if not self.simple_map.has_edge(*joined_intersections):
            st_name = tl.common_item(joined_intersections[0].connected_streets, joined_intersections[1].connected_streets)
            st_len = tl.distance_from_geo_coord(*joined_intersections[0].geo, *joined_intersections[1].geo)
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
    
    def add_sign_to_street(self, inter1, inter2, sign):
        for u,v,signs in self.simple_map.edges(data= signs):
            if u == inter1 and v == inter2:
                signs.append(sign)
                    
    def remove_street(self, street):
        pass
    
    def remove_sign_from_street(self, street, sign):
        pass
