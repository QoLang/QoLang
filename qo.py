import qstd
import qlexer
import qparser
from qclasses import BuiltinFunc, VarVal, Vars
Variables = Vars()
import qint
import sys

def run(args):
  # Load standard library
  for fn in qstd.available_functions:
    added = BuiltinFunc(fn, getattr(qstd, fn))
    Variables.setVar(added)

  contents = open(args[1]).read()
  lexer = qlexer.Lexer(contents)
  parser = qparser.Parser(lexer)
  interpreter = qint.Interpreter(parser, Variables)
  interpreter.interpret()

if __name__ == "__main__":
  run(sys.argv)