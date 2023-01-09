from source.agents.car import car
from source.agents.pilot import pilot
from source.ia.heuristics.euclidean_dist import euclidean_distance
from source.ia.heuristics.less_time import less_time
from source.ia.heuristics.more_profits import more_profit
from source.pilot_dsl.errors.error import runtime_error
from source.tools.reader import map_from_json
from source.pilot_dsl.builtins.pilang_callable import pilang_callable
from source.pilot_dsl.builtins.pilang_garage import pilang_gar
from typing import List, Any

class pilang_car(pilang_callable):
    
    def arity(self) -> int:
        return 2
    
    def call(self, interpreter, arguments: List[Any]):
        if not isinstance(arguments[0], int):
            raise runtime_error(arguments[0], f'{arguments[0]} most be an integer')
        
        _map = map_from_json("Map")
        cost_func = None
        heuristic = None
        client_selection = None
        _pilot = None
        
        match arguments[1]:
            case 'distance':
                cost_func = _map.distance_street_cost
                heuristic = euclidean_distance()
            case 'time':
                cost_func = _map.time_street_cost
                heuristic = less_time()
            case _:
                raise runtime_error(arguments[1], 'Inavalid argument')
            
        match arguments[2]:
            case 'profit':
                client_selection = more_profit()
            case _:
                raise runtime_error(arguments[2], 'Inavalid argument')
            
        if not isinstance(arguments[3], pilang_gar):
            raise runtime_error(arguments[3], f'{arguments[3]} most be garages')
        
        _pilot = pilot(cost_func, heuristic, client_selection, _map, arguments[3].garages)
        return car(arguments[0], _pilot)