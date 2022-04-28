import suslib
import sys

expression = open(sys.argv[1]).read()
lexer = suslib.Lexer(expression)
parser = suslib.Parser(lexer)
interpreter = suslib.Interpreter(parser)
interpreter.interpret()
print(interpreter.GLOBAL_SCOPE)