from math import sin, cos, sqrt, atan2, radians
from typing import List
from source.ia.k_means import k_means

import numpy as np

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
    longitude2 = radians(point2[1])
    
    dlat = latitude2 - latitude1
    dlon = longitude2 - longitude1
    
    a = sin(dlat / 2)**2 + cos(latitude1) * cos(latitude2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return round(6373.0 * c * 1000,1) 

def get_garages_loc(_map, garages_count : int):
    
    _k_means = k_means()
    garages_intersections = _k_means.evaluate(_map.intersections, garages_count, 100)
    result = []
    for _intersection in garages_intersections:
        result.append(from_intersection_to_street(_map, _intersection))
    return result

def from_intersection_to_street(_map, garage):
    from source.environment._map import street
    
    adjacent = _map.adj_dict[garage]
    nearest_intersection = None
    lower_distance = np.inf
    for _intersection in adjacent:
        distance = distance_from_geo_coord(garage.geo_coord, _intersection.geo_coord)
        if distance < lower_distance:
            lower_distance = distance
            nearest_intersection = _intersection
            
    return street(garage,nearest_intersection)