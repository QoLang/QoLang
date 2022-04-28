import suslib
import sys

expression = open(sys.argv[1]).read()
lexer = suslib.Lexer(expression)
parser = suslib.Parser(lexer)
interpreter = suslib.Interpreter(parser)
interpreter.interpret()
out = ""
for val in suslib.Variables.vars:
  if isinstance(val, suslib.VarVal):
    out += f"{val.name}: {val.value}\n"
out = out[:-1]

print(out)