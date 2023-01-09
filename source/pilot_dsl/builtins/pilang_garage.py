from source.pilot_dsl.errors.error import runtime_error
from source.tools.reader import map_from_json
from source.tools.general_tools import get_garages_loc
from source.pilot_dsl.builtins.pilang_callable import pilang_callable
from typing import List, Any

class pilang_gar(pilang_callable):
    
    def arity(self) -> int:
        return 1
    
    def call(self, interpreter, arguments: List[Any]):
        if not isinstance(arguments[0], int):
            raise runtime_error(arguments[0], f'{arguments[0]} most be an integer')
        return get_garages_loc(map_from_json("Map"), arguments[0])