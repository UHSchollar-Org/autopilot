from source.simulation.simulation import simulation
from source.tools.reader import map_from_json
from source.pilot_dsl.builtins.pilang_callable import pilang_callable
from typing import List, Any

class pilang_sim(pilang_callable):
    
    def arity(self) -> int:
        return 3
    
    def call(self, interpreter, arguments: List[Any]):
        return simulation(map_from_json("Map"),arguments[0],len(arguments[0]),arguments[1],arguments[2])