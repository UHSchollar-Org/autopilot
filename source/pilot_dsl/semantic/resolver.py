from source.pilot_dsl.lexer.token_ import token
from source.pilot_dsl.ast.expressions import *
from source.pilot_dsl.ast.statements import *
from source.pilot_dsl.interpreter.interpreter import interpreter
from collections import deque
from typing import List, Deque, Dict
from source.pilot_dsl.builtins.pilang_func import function_type
from source.pilot_dsl.builtins.pilang_class import class_type

class resolver(stmt_visitor, exp_visitor):
    def __init__(self, interpreter : interpreter, on_error = None) -> None:
        self.interpreter = interpreter
        self.scopes : Deque[Dict[str, bool]] = deque()
        self.on_error = on_error
        self.current_func = function_type.NONE
        self.current_class = class_type.NONE
    
    #region Other Methods
    
    def resolve_local(self, expression : expression, name : token):
        for i, scope in enumerate(reversed(self.scopes)):
            if name.lexeme in scope:
                self.interpreter.resolve(expression, i)
                return
        # Not found. Assume it is global. 
    
    def resolve_single_exp(self, expression : expression):
        expression.validate(self)
        
    def resolve_single_stmt(self, statement : statement):
        statement.validate(self)
    
    def resolve_stmts(self, statements : List[statement]):
        for stmt in statements:
            self.resolve_single_stmt(stmt)
    
    def resolve(self, statements : List[statement]):
        self.resolve_stmts(statements)
    
    def resolve_func(self, func : function_stmt, func_type : function_type):
        enclosing_func = self.current_func
        self.current_func = func_type
        
        self.begin_scope()
        
        for param in func.params:
            self.declare(param)
            self.define(param)
        
        self.resolve_stmts(func.body)
        self.end_scope()
        self.current_func = enclosing_func
    
    def begin_scope(self):
        self.scopes.append({})
    
    def end_scope(self):
        self.scopes.pop()
    
    def declare(self, name : token):
        if len(self.scopes) == 0:
            return
        
        scope = self.scopes[-1]
        if name.lexeme in scope:
            self.on_error(name, "Already variable with this name in this scope.")
        
        scope[name.lexeme] = False
    
    def define(self, name : token):
        if len(self.scopes) == 0:
            return
        
        scope = self.scopes[-1]
        scope[name.lexeme] = True
    #endregion
    
    #region visit_exps
    
    def visit_var_exp(self, exp: var_exp):
        if len(self.scopes) != 0 and self.scopes[-1].get(exp.name.lexeme) is False:
            self.on_error(exp.name, "Cannot read local variable in its own initializer.")
        
        self.resolve_local(exp, exp.name)
    
    def visit_assign_exp(self, exp: assign_exp):
        self.resolve_single_exp(exp.value)
        self.resolve_local(exp, exp.name)
    
    def visit_binary_exp(self, exp: binary_exp):
        self.resolve_single_exp(exp.left_exp)
        self.resolve_single_exp(exp.right_exp)
    
    def visit_call_exp(self, exp: call_exp):
        self.resolve_single_exp(exp.callee)
        
        for arg in exp.args:
            self.resolve_single_exp(arg)
    
    def visit_grouping_exp(self, exp: grouping_exp):
        self.resolve_single_exp(exp.exp)

    def visit_literal_exp(self, exp: literal_exp):
        return 
    
    def visit_logical_exp(self, exp: logical_exp):
        self.resolve_single_exp(exp.left_exp)
        self.resolve_single_exp(exp.right_exp)
    
    def visit_unary_exp(self, exp: unary_exp):
        self.resolve_single_exp(exp.exp)
    
    def visit_get_exp(self, exp: get_exp):
        self.resolve_single_exp(exp.object)
    
    def visit_set_exp(self, exp: set_exp):
        self.resolve_single_exp(exp.value)
        self.resolve_single_exp(exp.object)
    
    def visit_father_exp(self, exp: father_exp):
        if self.current_class == class_type.NONE:
            self.on_error(exp.keyword, "Can't use 'father' outside of a class.")

        elif self.current_class != class_type.SUBCLASS:
            self.on_error(exp.keyword, "Can't use 'father' in a class with no father_class.")
        
        self.resolve_local(exp, exp.keyword)
    
    def visit_this_exp(self, exp: this_exp):
        if self.current_class == class_type.NONE:
            self.on_error(exp.keyword, "Can't use 'this' outside of a class.")
        
        self.resolve_local(exp, exp.keyword)
    
    #endregion
    
    #region visit_stmts
    
    def visit_block_stmt(self, stmt: block_stmt):
        self.begin_scope()
        self.resolve_stmts(stmt.statements)
        self.end_scope()
    
    def visit_var_stmt(self, stmt: var_stmt):
        self.declare(stmt.name)
        
        if stmt.initializer is not None:
            self.resolve_single_exp(stmt.initializer)
        
        self.define(stmt.name)
    
    def visit_function_stmt(self, stmt: function_stmt):
        self.declare(stmt.name)
        self.define(stmt.name)
        
        self.resolve_func(stmt, function_type.FUNCTION)
    
    def visit_expression_stmt(self, stmt: expression_stmt):
        self.resolve_single_exp(stmt.expression)
    
    def visit_if_stmt(self, stmt: if_stmt):
        self.resolve_single_exp(stmt.condition)
        self.resolve_single_stmt(stmt.then_branch)
        
        if stmt.else_branch:
            self.resolve_single_stmt(stmt.else_branch)
    
    def visit_print_stmt(self, stmt: print_stmt):
        self.resolve_single_exp(stmt.expression)
    
    def visit_return_stmt(self, stmt: return_stmt):
        if self.current_func == function_type.NONE:
            self.on_error(stmt.keyword, "Can't return from top-level code.")
        
        if stmt.value:
            if self.current_func == function_type.INITIALIZER:
                self.on_error(stmt.keyword, "Can't return a value from an initializer.")
            
            self.resolve_single_exp(stmt.value)
    
    def visit_while_stmt(self, stmt: while_stmt):
        self.resolve_single_exp(stmt.condition)
        self.resolve_single_stmt(stmt.body)
    
    def visit_class_stmt(self, stmt: class_stmt):
        enclosing_class = self.current_class
        self.current_class = class_type.CLASS
        
        self.declare(stmt.name)
        self.define(stmt.name)
        
        if stmt.father_class and stmt.name.lexeme == stmt.father_class.name.lexeme:
            self.on_error(stmt.father_class.name, "A class can't inherit from itself.")
        
        if stmt.father_class is not None:
            self.current_class = class_type.SUBCLASS
            self.resolve_single_exp(stmt.father_class)
        
        if stmt.father_class is not None:    
            self.begin_scope()
            self.scopes[-1]["father"] = True
        
        self.begin_scope()
        self.scopes[-1]["this"] = True
        
        for mtd in stmt.methods:
            decl = function_type.METHOD
            
            if mtd.name.lexeme == "init":
                decl = function_type.INITIALIZER
            
            self.resolve_func(mtd, decl)
        
        self.end_scope()
        
        if stmt.father_class is not None:
            self.end_scope()
        
        self.current_class = enclosing_class
        
    #endregion