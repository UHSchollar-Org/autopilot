import pathlib as pl
import json
from source.environment._map import *

def back_path(path: str, steps):
    for i in range(path.__len__()-1 , -1, -1):
        if path[i] == "\\":
            steps-=1
            if steps == 0:
                return path[:i]
            
def get_config_path():
    reader_path = pl.Path(__file__).parent.absolute()
    root_path = back_path(str(reader_path),2)
    return root_path + "\\json"
    
def map_from_json(map_name) -> map:
    path = get_config_path() + "\\map_config.json"
    raw_map = map(map_name)
    
    with open(path, 'r') as f:
        j_map = json.load(f)
        
        for s in j_map['streets']:
            signs = s['traffic_signs']
            inter1 = intersection(s['intersection1'], s['geo_coord_1'])
            inter2 = intersection(s['intersection2'], s['geo_coord_2'])
            
            raw_map.add_street(signs, (inter1,inter2))
    
    return raw_map