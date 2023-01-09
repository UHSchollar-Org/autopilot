from __future__ import annotations
from source.pilot_dsl.interpreter.namespace import scope
from .pilang_callable import pilang_callable
from source.pilot_dsl.ast.statements import function_stmt
from typing import List, Any
from source.pilot_dsl.errors.error import return_error
from enum import Enum, auto
from .pilang_instance import pilang_instance
from source.pilot_dsl.builtins.pilang_func import pilang_func
from source.simulation.simulation import simulation
from source.tools.reader import map_from_json

class pilang_run_sim(pilang_func):
    def __init__(self, declaration : function_stmt, closure : scope, is_init : bool) -> None:
        super().__init__(declaration,closure,is_init)
        
    def call(self, interpreter, arguments: List[Any]):
        _scope = scope(self.closure)
        cars = []
        for i in range(2,len(arguments)):
            cars.append(arguments[i])
        _simulation = simulation(map_from_json("Map"),cars, len(cars), arguments[0].garages, arguments[1])
        results = _simulation.run()
        
        _scope.define('simulation', _simulation)
        
        print(f'Clients picked up:')
        for car in results['cars_pickups'].keys():
            print(f'{car} : {results["cars_pickups"][car]}')
        print(f'Earned money:')
        for car in results['cars_money'].keys():
            print(f'{car} : {results["cars_money"][car]}')
        print(f'Manteinance expenses:')
        for car in results["cars_manteinance"].keys():
            print(f'{car} : {results["cars_manteinance"][car]}')
        
        if self.is_init:
            return self.closure.get_at(0, "this")
        
    def arity(self) -> int:
        return 4
    
    def bind(self, instance : pilang_instance) -> pilang_run_sim:
        _scope = scope(self.closure)
        _scope.define("this", instance)
        return pilang_run_sim(self.declaration, _scope, self.is_init)