from source.agents.pilot import pilot
from source.ia.heuristics.euclidean_dist import euclidean_distance
from source.ia.heuristics.less_time import less_time
from source.ia.heuristics.more_profits import more_profit
from source.pilot_dsl.errors.error import runtime_error
from source.tools.reader import map_from_json
from source.pilot_dsl.builtins.pilang_callable import pilang_callable
from source.pilot_dsl.builtins.pilang_garage import pilang_gar
from typing import List, Any

class pilang_strat(pilang_callable):
    
    def arity(self) -> int:
        return 3
    
    def call(self, interpreter, arguments: List[Any]):
        _map = map_from_json("Map")
        cost_func = None
        heuristic = None
        client_selection = None
        
        match arguments[0]:
            case 'distance':
                cost_func = _map.distance_street_cost
                heuristic = euclidean_distance()
            case 'time':
                cost_func = _map.time_street_cost
                heuristic = less_time()
            case _:
                raise runtime_error(arguments[0], 'Inavalid argument')
            
        match arguments[1]:
            case 'profit':
                client_selection = more_profit()
            case _:
                raise runtime_error(arguments[1], 'Inavalid argument')
            
        if not isinstance(arguments[2], pilang_gar):
            raise runtime_error(arguments[2], f'{arguments[2]} most be garages')
                
        return pilot(cost_func, heuristic, client_selection, _map, arguments[2].garages)