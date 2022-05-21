import qstd
import qlexer
import qparser
from qclasses import BuiltinFunc, Variables, VarVal
import qint
import sys

# Load standard library
for fn in qstd.available_functions:
  added = BuiltinFunc(fn, getattr(qstd, fn))
  Variables.setVar(added)

expression = open(sys.argv[1]).read()
lexer = qlexer.Lexer(expression)
parser = qparser.Parser(lexer)
interpreter = qint.Interpreter(parser)
interpreter.interpret()

#tok = lexer.next_token()
#while tok.value is not None:
#  print(tok)
#  tok = lexer.next_token()

sys.exit() # Remove/comment this line if you want to see variables

out = ""
for val in Variables.vars:
  if isinstance(val, VarVal):
    out += f"{val.name}: {val.value}\n"
out = out[:-1]

print(out)