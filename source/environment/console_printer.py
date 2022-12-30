from source.environment._map import *

def print_streets(map: map):
    for street in map.streets:
        print(street)
                
def print_signs(map: map):
    for street in map.streets:
        print(f'street: {street} <signs : {street.traffic_signs}>')
        

def print_street_len(map : map):
    for street in map.streets:
        print(f'street: {street} <length : {street.length}>')