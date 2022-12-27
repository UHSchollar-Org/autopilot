from source.pilot_dsl.lexer.token_ import token
from source.pilot_dsl.ast.expressions import *
from source.pilot_dsl.ast.statements import *
from source.pilot_dsl.interpreter.interpreter import interpreter
from collections import deque
from typing import List, Deque

class resolver(stmt_visitor, exp_visitor):
    def __init__(self, interpreter : interpreter, on_error = None) -> None:
        self.interpreter = interpreter
        self.scopes : Deque = deque()
        self.on_error = on_error
        