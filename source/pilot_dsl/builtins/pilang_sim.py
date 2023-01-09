from source.simulation.simulation import simulation
from source.agents.car import car
from source.tools.reader import map_from_json
from source.pilot_dsl.builtins.pilang_callable import pilang_callable
from source.pilot_dsl.builtins.pilang_garage import pilang_gar
from typing import List, Any
from source.pilot_dsl.errors.error import runtime_error

class pilang_sim(pilang_callable):
    
    def arity(self) -> int:
        return 3
    
    def call(self, interpreter, arguments: List[Any]):
        if not isinstance(arguments[0], pilang_gar):
            raise runtime_error(arguments[1], f'{arguments[1]} most be garages')
        if not isinstance(arguments[1], int):
            raise runtime_error(arguments[2], f'{arguments[2]} most be an integer')
        
        cars = []
        for i in range(2,len(arguments)):
            if not isinstance(arguments[i], car):
                raise runtime_error(arguments[i], f'{arguments[i]} most be a car')
            cars.append(arguments[i])
        return simulation(map_from_json("Map"),cars, len(cars), arguments[0].garages, arguments[1])