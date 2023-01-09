from source.agents.car import car
from source.agents.pilot import pilot
from source.pilot_dsl.errors.error import runtime_error
from source.tools.reader import map_from_json
from source.pilot_dsl.builtins.pilang_callable import pilang_callable
from typing import List, Any

class pilang_car(pilang_callable):
    
    def arity(self) -> int:
        return 2
    
    def call(self, interpreter, arguments: List[Any]):
        if not isinstance(arguments[0], int):
            raise runtime_error(arguments[0], f'{arguments[0]} most be an integer')
        if not isinstance(arguments[1], pilot):
            raise runtime_error(arguments[1], f'{arguments[1]} most be a strategy')
        
        return car(arguments[0], arguments[1])