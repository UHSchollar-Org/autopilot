from typing import List, Any, Dict
from source.pilot_dsl.ast.expressions import *
from source.pilot_dsl.lexer.token_ import *
from source.pilot_dsl.lexer.static_data import token_type
from source.pilot_dsl.errors.error import runtime_error, return_error
from source.pilot_dsl.ast.statements import *
from source.pilot_dsl.interpreter.namespace import scope
from source.pilot_dsl.builtins.pilang_callable import pilang_callable
from source.pilot_dsl.builtins.pilang_func import pilang_func
from source.pilot_dsl.builtins.pilang_instance import pilang_instance
from source.pilot_dsl.builtins.pilang_class import pilang_class
from source.pilot_dsl.builtins.pilang_sim import pilang_sim
from source.pilot_dsl.builtins.pilang_car import pilang_car
from source.pilot_dsl.builtins.pilang_garage import pilang_gar
from source.pilot_dsl.builtins.pilang_run_sim import pilang_run_sim
from structlog import get_logger

log = get_logger()

class interpreter(exp_visitor, stmt_visitor):
    
    def __init__(self) -> None:
        self.globals = scope()
        self.scope = self.globals
        self.locals = {}
        
        #self.globals.define('simulation', pilang_sim())
        self.globals.define('car', pilang_car()) 
        self.globals.define('garages', pilang_gar())      
        
        self.globals.define('simulation', None)
        methods : Dict[str, pilang_sim] = {}
        methods['init'] = pilang_run_sim(None, self.globals, True)
        
        _class = pilang_sim(methods)
        self.globals.assign(token(token_type.IDENTIFIER,'simulation',None,0), _class)
        
    #region others_methods
    
    @staticmethod
    def is_truthy(obj):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        #is digit
        return True
    
    @staticmethod
    def binary_plus(exp, left, right):
        if isinstance(left, (float, int)) and isinstance(right, (float, int)):
            return left + right
        
        if isinstance(left, str) and isinstance(right, str):
            return str(left + right)
        
        raise runtime_error(exp.operator, f'{left} and {right} must be two numbers or two strings.')
    
    @staticmethod
    def is_equal(a, b):
        if a is None:
            if b is None:
                return True
            return False
        return a == b
    
    @staticmethod
    def check_number_operand(operator : token, operand):
        if isinstance(operand, (float, int)):
            return
        raise runtime_error(operator, f'{operand} must be a number')
    
    @staticmethod
    def check_number_operands(operator : token, left, right):
        if isinstance(left, (float, int)) and isinstance(right, (float, int)):
            return
        raise runtime_error(operator, f'{left} and {right} must be numbers.')
    
    @staticmethod
    def stringify(obj):
        if obj is None:
            return 'null'
        
        if isinstance(obj, float):
            return f'{obj:0.6f}'.rstrip('0').rstrip('.')
        
        return str(obj)
    
    def execute(self, stmt : statement):
        return stmt.validate(self)
    
    def exec_block(self, statements : List[statement], scope : scope):
        previous_scope = self.scope
        try:
            self.scope = scope
            
            for stmt in statements:
                self.execute(stmt)
        finally:
            self.scope = previous_scope
    
    def resolve(self, exp : expression, depth : int):
        self.locals[exp] = depth
    
    def look_up_var(self, name : token, exp : expression) -> Any:
        dist = self.locals.get(exp)
        if dist is not None:
            return self.scope.get_at(dist, name.lexeme)
        else:
            return self.globals.get(name)
    
    #endregion
    
    #region expressions_visit
    
    def evaluate(self, exp : expression):
        return exp.validate(self)
    
    def visit_literal_exp(self, exp: literal_exp):
        return exp.value
    
    def visit_grouping_exp(self, exp: grouping_exp):
        return self.evaluate(exp.exp)
    
    def visit_unary_exp(self, exp: unary_exp):
        right = self.evaluate(exp.exp)
        
        t_type = exp.operator.type
      
        match t_type:
            case token_type.MINUS:
                self.check_number_operand(exp.operator, right)
                return -float(right)
            
            case token_type.NOT:
                return not self.is_truthy(right)
        
        return None
    
    def visit_binary_exp(self, exp: binary_exp):
        left = self.evaluate(exp.left_exp)
        right = self.evaluate(exp.right_exp)
        
        if exp.operator.type not in (token_type.PLUS, token_type.NOT_EQUAL, token_type.EQUAL_EQUAL):
            self.check_number_operands(exp.operator, left, right)
        
        match exp.operator.type:
            case token_type.MINUS:
                return float(left) - float(right)
            
            case token_type.SLASH:
                return float(left) / float(right)
            
            case token_type.ASTERISK:
                return float(left) * float(right)
            
            case token_type.PLUS:
                return self.binary_plus(exp, left, right)
                
            case token_type.GREATER:
                return float(left) > float(right)
            
            case token_type.GREATER_EQUAL:
                return float(left) >= float(right)
                
            case token_type.LESS:
                return float(left) < float(right)
            
            case token_type.LESS_EQUAL:
                return float(left) <= float(right)
                
            case token_type.NOT_EQUAL:
                return not self.is_equal(left, right) 
            
            case token_type.EQUAL_EQUAL:
                return self.is_equal(left, right)
        
        raise runtime_error(exp.operator, f'Unknown operator {exp.operator.lexeme}')
    
    def visit_var_exp(self, exp: var_exp):
        return self.look_up_var(exp.name, exp)
    
    def visit_logical_exp(self, exp: logical_exp):
        left = self.evaluate(exp.left_exp)
        
        if exp.operator.type == token_type.OR:
            if self.is_truthy(left):
                return left
        elif not self.is_truthy(left):
            return left
        
        return self.evaluate(exp.right_exp)
    
    def visit_call_exp(self, exp: call_exp):
        func = self.evaluate(exp.callee)
        
        args = [self.evaluate(arg) for arg in exp.args]
        
        if not isinstance(func, pilang_callable):
            raise runtime_error(exp.paren, 'Can only call functions and classes.')
        
        if len(args) != func.arity():
            raise runtime_error(exp.paren, f'Expected {func.arity()} arguments but got {len(args)}.')
        
        return func.call(self, args)
   
    def visit_assign_exp(self, exp: assign_exp):
        value = self.evaluate(exp.value)
        
        distance = self.locals.get(exp)
        
        if distance:
            self.scope.assign_at(distance, exp.name, value)
        else:
            self.globals.assign(exp.name, value)
        
        return value
       
    def visit_get_exp(self, exp: get_exp):
        obj = self.evaluate(exp.object)
        
        if isinstance(obj, pilang_instance):
            return obj.get(exp.name)
        
        raise runtime_error(exp.name, "Only instances have properties.") 
    
    def visit_set_exp(self, exp: set_exp):
        obj = self.evaluate(exp.object)
        
        if not isinstance(obj, pilang_instance):
            raise runtime_error(exp.name, "Only instances have fields.")
        
        value = self.evaluate(exp.value)
        obj.set(exp.name, value)
        return value
    
    def visit_father_exp(self, exp: father_exp):
        dist = self.locals[exp]
        
        father_class : pilang_class = self.scope.get_at(dist, "father")
        
        obj = self.scope.get_at(dist - 1, "this")
        mtd = father_class.find_method(exp.method.lexeme)
        
        if mtd is None:
            raise runtime_error(exp.method, f'Undefined property \'{exp.method.lexeme}\'.')
        
        return mtd.bind(obj)
    
    def visit_this_exp(self, exp: this_exp):
        return self.look_up_var(exp.keyword, exp)
    
    #endregion
    
    #region statements_visit
    
    def visit_expression_stmt(self, stmt: expression_stmt):
        return self.evaluate(stmt.expression)
    
    def visit_print_stmt(self, stmt: print_stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
    
    def visit_var_stmt(self, stmt: var_stmt):
        value = None
        
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
            
        self.scope.define(stmt.name.lexeme, value)
    
    def visit_block_stmt(self, stmt: block_stmt):
        self.exec_block(self, stmt.statements, scope(self.scope))
    
    def visit_if_stmt(self, stmt: if_stmt):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)
    
    def visit_while_stmt(self, stmt: while_stmt):
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
    
    def visit_function_stmt(self, stmt: function_stmt):
        func = pilang_func(stmt, self.scope, False)
        
        self.scope.define(stmt.name.lexeme, func)
    
    def visit_return_stmt(self, stmt: return_stmt):
        value = None
        
        if stmt.value:
            value = self.evaluate(stmt.value)
        
        raise return_error(value)
    
    def visit_class_stmt(self, stmt: class_stmt):
        father_class = None
        
        if stmt.father_class is not None:
            father_class = self.evaluate(stmt.father_class)
            
            if not isinstance(father_class, pilang_class):
                raise runtime_error(stmt.father_class.name, "Father_class must be a class.")
            
        self.scope.define(stmt.name.lexeme, None)
        
        if stmt.father_class is not None:
            self.scope = scope(self.scope)
            self.scope.define("father", father_class)
        
        methods : Dict[str, pilang_func] = {}
        
        for mtd in stmt.methods:
            func = pilang_func(mtd, self.scope, mtd.name.lexeme == "init")
            methods[mtd.name.lexeme] = func
        
        _class = pilang_class(stmt.name.lexeme, father_class, methods)
        
        if stmt.father_class is not None:
            self.scope = self.scope.enclosing
        
        self.scope.assign(stmt.name, _class)
        
    
    #endregion
    
    def interpret(self, statements : List[statement], on_error = None) -> Any:
        try:
            res = None
            for stmt in statements:
                #log.debug("Executing", stmt)
                res = self.execute(stmt)
            
            #return res #for testing and debugging
        except runtime_error as run_error:
            on_error(run_error)
                