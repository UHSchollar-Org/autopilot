# ast_printer class is used to print the AST tree, which is used for debugging purpose only.
# The class is a subclass of exp_visitor, which is used to visit each node in the AST tree.
# and for print the ast tree, we need to call the print method of ast_printer class.

from source.pilot_dsl.ast.expressions import *

class ast_printer(exp_visitor):
    
    def visit_assign(self, exp: assign_exp):
        return super().visit_assign(exp)
    
    def visit_binary(self, exp: binary_exp):
        return self.parenthesis(exp.operator.lexeme, exp.left_exp, exp.right_exp)
    
    def visit_call(self, exp: call_exp):
        return super().visit_call(exp)
    
    def visit_get(self, exp: get_exp):
        return super().visit_get(exp)
    
    def visit_grouping(self, exp: grouping_exp):
        return self.parenthesis("group", exp.exp)
    
    def visit_literal(self, exp: literal_exp):
        return "null" if exp.value is None else str(exp.value)
    
    def visit_logical(self, exp: logical_exp):
        return super().visit_logical(exp)
    
    def visit_set(self, exp: set_exp):
        return super().visit_set(exp)
    
    def visit_father(self, exp: father_exp):
        return super().visit_father(exp)
    
    def visit_this(self, exp: this_exp):
        return super().visit_this(exp)
    
    def visit_unary(self, exp: unary_exp):
        return self.parenthesis(exp.operator.lexeme, exp.exp)
    
    def visit_var(self, exp: var_exp):
        return super().visit_var(exp)
    
    def print(self, exp : expression) -> str:
        return exp.validate(self)
    
    def parenthesis(self, name : str, *args : expression):
        
        exps = ["(", name]
        
        for arg in args:
            exps.append(" ")
            exps.append(arg.validate(self))
        
        exps.append(")")
        
        return "".join(exps)