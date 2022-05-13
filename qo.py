import qolib
import qint
import sys

expression = open(sys.argv[1]).read()
lexer = qolib.Lexer(expression)
parser = qolib.Parser(lexer)
interpreter = qint.Interpreter(parser)
interpreter.interpret()

exit() # Remove/comment this line if you want to see variables

out = ""
for val in qolib.Variables.vars:
  if isinstance(val, qolib.VarVal):
    out += f"{val.name}: {val.value}\n"
out = out[:-1]

print(out)