import qstd
import qlexer
import qparser
from qclasses import PythonFunc, VarVal, Vars
Variables = Vars()
import qint
import sys

def run(args):
  # Load standard library
  for fn in qstd.qolang_export:
    if callable(getattr(qstd, fn)):
      added = PythonFunc(fn, getattr(qstd, fn))
    else:
      added = VarVal(fn, getattr(qstd, fn))
    Variables.setVar(added)

  contents = open(args[1]).read()
  lexer = qlexer.Lexer(contents)
  parser = qparser.Parser(lexer)
  interpreter = qint.Interpreter(parser, Variables, args[1])
  interpreter.interpret()

if __name__ == "__main__":
  run(sys.argv)