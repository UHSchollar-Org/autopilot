from source.simulation.simulation import simulation
from source.tools.reader import map_from_json
from source.pilot_dsl.builtins.pilang_callable import pilang_callable
from source.pilot_dsl.builtins.pilang_garage import pilang_gar
from typing import List, Any
from source.pilot_dsl.errors.error import runtime_error

class pilang_sim(pilang_callable):
    
    def arity(self) -> int:
        return 3
    
    def call(self, interpreter, arguments: List[Any]):
        if not isinstance(arguments[0], int):
            raise runtime_error(arguments[0], f'{arguments[0]} most be an integer')
        if not isinstance(arguments[1], pilang_gar):
            raise runtime_error(arguments[1], f'{arguments[1]} most be garages')
        if not isinstance(arguments[2], int):
            raise runtime_error(arguments[2], f'{arguments[2]} most be an integer')
        return simulation(map_from_json("Map"),arguments[0],len(arguments[0]),arguments[1].garages, arguments[2])