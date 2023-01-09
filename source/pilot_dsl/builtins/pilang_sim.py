from source.pilot_dsl.builtins.pilang_class import pilang_class
from source.pilot_dsl.builtins.pilang_func import pilang_func
from .pilang_instance import pilang_instance
from typing import List, Any, Dict

class pilang_sim(pilang_class):
    
    def __init__(self, methods: Dict[str, pilang_func]) -> None:
        super().__init__('simulation', None , methods)
    
    def arity(self) -> int:
        return 4
    
    def call(self, interpreter, arguments: List[Any]):
        instance = pilang_instance(self)
        init = self.find_method("init")
        
        if init:
            init.bind(instance).call(interpreter, arguments)
        
        return instance
    