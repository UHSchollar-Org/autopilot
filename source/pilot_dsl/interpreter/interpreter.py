
from source.pilot_dsl.ast.expressions import *
from source.pilot_dsl.lexer.token_ import *
from source.pilot_dsl.lexer.static_data import token_type
from source.pilot_dsl.errors.error import runtime_error

class interpreter(exp_visitor):
    
    def __init__(self) -> None:
        super().__init__()
    
    def evaluate(self, exp : expression):
        return exp.validate(self)
    
    @staticmethod
    def is_truthy(obj):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
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
    
    def visit_literal(self, exp: literal_exp):
        return exp.value
    
    def visit_grouping(self, exp: grouping_exp):
        return self.evaluate(exp.exp)
    
    def visit_unary(self, exp: unary_exp):
        right = self.evaluate(exp.exp)
        
        t_type = exp.operator.type
      
        match t_type:
            case token_type.MINUS:
                self.check_number_operand(exp.operator, right)
                return -float(right)
            
            case token_type.NOT:
                return not self.is_truthy(right)
        
        return None
    
    def visit_binary(self, exp: binary_exp):
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
            
        return None
    
    def interpret(self, exp : expression):
        try:
            value = self.evaluate(exp)
            print(self.stringify(value))
        except runtime_error as e:
            print(e.message)
            print(f'line {e.token.line} column {e.token.column}')
            return False
        return True
                    
        
        
    