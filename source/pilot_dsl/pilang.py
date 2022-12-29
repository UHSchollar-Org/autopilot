import sys
from structlog import get_logger
from source.pilot_dsl.interpreter.interpreter import interpreter
from source.pilot_dsl.parser.parser_ll import parser_ll
from source.pilot_dsl.semantic.resolver import resolver
from source.pilot_dsl.lexer.lexer import lexer
from source.pilot_dsl.lexer.token_ import token
from source.pilot_dsl.lexer.static_data import token_type
from source.pilot_dsl.errors.error import runtime_error

log = get_logger()

class pilang:
    def __init__(self) -> None:
        self.error : bool = False
        self.runtime_error : bool = False
        self.interpreter : interpreter = interpreter()
    
    def run(self, source : str):
        log.debug("Running line", source = source)

        _lexer = lexer(source, self.report_error)
        tokens : list[token] = _lexer.tokenize()
        
        for token in tokens:
            log.debug("Token", token = token)
        
        _parser = parser_ll(tokens, self.token_error)
        stmts = _parser.parse()
        
        # Stop if there was a syntax error.
        if self.error:
            log.debug("Error after parsing.")
            return
        
        _resolver = resolver(self.interpreter, self.token_error)
        _resolver.resolve(stmts)
        
        # Stop if there was a resolution error.
        if self.error:
            log.debug("Error after semantic analysis")
            return

        self.interpreter.interpret(stmts, self.report_runtime_error)
        
    def report_error(self, line : int, message : str):
        self.report(line, "", message)
    
    def report(self, line : int, where : str, message : str):
        message = f"[line {line}] Error{where}: {message}"
        log.warning(message)
        print(message, file=sys.stderr)
        self.error = True

    def token_error(self, token : token, message : str):
        if token.type == token_type.EOF:
            self.report(token.line, " at end", message)
        else:
            self.report(token.line, f" at '{token.lexeme}'", message)
    
    def report_runtime_error(self, error : runtime_error):
        msg = f"{str(error.message)} at line [line {error.token.line}]"
        
        log.warning(msg)
        print(msg, file=sys.stderr)
        self.runtime_error = True
    
    @staticmethod
    def load_file(file_path : str):
        with open(file_path, "r") as f:
            text = f.readlines()
            lines = '\n'.join(text)
            return lines
    
    def run_file(self, file_path : str):
        source = pilang.load_file(file_path)
        self.run(source)
        
        if self.error:
            sys.exit(65)
            
        if self.runtime_error:
            sys.exit(70)
    
    def quit(self):
        print("Goodbye!")
        sys.exit(0)
      
    def run_prompt(self):
        print("Pilang v0.1.0")
        print("Press Ctrl+C or Ctrl+D to exit.")
        
        while True:
            try:
                prompt = input(">>> ")
                if prompt and prompt[0] == chr(4):
                    raise EOFError
                
                self.run(prompt)
                self.error = False
            except (KeyboardInterrupt, EOFError):
                self.quit()
    
    @staticmethod
    def main():
        if len(sys.argv) > 2:
            print(f"Usage: {sys.argv[0]} [script]")
            sys.exit(64)
        elif len(sys.argv) == 2:
            pilang().run_file(sys.argv[1])
        else:
            pilang().run_prompt()