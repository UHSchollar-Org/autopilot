from math import sin, cos, sqrt, atan2, radians

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
            
def distance_from_geo_coord(latitude1, longitude1, latitude2, longitude2) -> float:
    latitude1 = radians(latitude1)
    longitude1 = radians(longitude1)
    latitude2 = radians(latitude2)
    longitude2 = radians(longitude2)
    
    dlat = latitude2 - latitude1
    dlon = longitude2 - longitude1
    
    a = sin(dlat / 2)**2 + cos(latitude1) * cos(latitude2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return round(6373.0 * c * 1000,1) 
        