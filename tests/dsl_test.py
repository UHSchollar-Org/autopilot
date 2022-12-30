from tests.generic_test import test
from source.pilot_dsl.lexer.lexer import lexer


class dsl_test(test):
    pilang_code1 = """
class A 
{
    var a = 3;
    var b = true; 
    func t(param1, param2)
    {
        return a or b;
    }
}"""
        
    pilang_code2 = """
class A
{
    var r = false;
    var d23 = true;
    var t = 909090;
    
    func r(param1, param2, param3)
    {
        var y = this.r and this.d23;
        return y;    
    }
}            
class B < A 
{
    func printer()
    {
        print "Hi, i am a son of A"
    }    
}"""
    
    codes = [pilang_code1, pilang_code2]
    
    def run_test(self):
        for code in self.codes:
            print(f'Testing code {code[len(code) - 1]}:\n')
            print(code)
            print('\n')
            l = lexer(code)
            for tok in l.tokens:
                print(tok)
            
        