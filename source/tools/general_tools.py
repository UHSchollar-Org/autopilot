from math import sin, cos, sqrt, atan2, radians
from source.environment._map import intersection, street
from typing import List

def same_items(list1, list2) -> bool:
    if len(list1) != len(list2):
        return False
    for item in list1:
        if item not in list2:
            return False
    return True

def common_item(list1, list2) -> str:
    for i1 in list1:
        for i2 in list2:
            if i1 == i2:
                return i1
            
def distance_from_geo_coord(point1 : tuple, point2 : tuple)-> float:
    latitude1 = radians(point1[0])
    longitude1 = radians(point1[1])
    latitude2 = radians(point2[0])
    longitude2 = radians(point2)
    
    dlat = latitude2 - latitude1
    dlon = longitude2 - longitude1
    
    a = sin(dlat / 2)**2 + cos(latitude1) * cos(latitude2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return round(6373.0 * c * 1000,1) 

def from_intersections_to_streets(intersections : List[intersection]) -> List[street]:
    """Dada una lista de intersecciones devuelve la lista de calles que forman
    """
    result : List[street] = []
    for i in range(1,len(intersections)):
        result.append(street(intersections[i-1]),street(intersections[i]))
    return result
        