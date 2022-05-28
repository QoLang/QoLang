import qlexer
import qparser
from qclasses import PythonFunc, VarVal, Vars
Variables = Vars()
import qint
import sys
import runpy

def run(args):
  # Load standard library
  toinclude = runpy.run_path("/usr/lib/qo/std.py")
  for fn in toinclude["qolang_export"]:
    if callable(toinclude[fn]):
      added = PythonFunc(fn, toinclude[fn])
    else:
      added = VarVal(fn, toinclude[fn])
    Variables.setVar(added)

  contents = open(args[1]).read()
  lexer = qlexer.Lexer(contents)
  parser = qparser.Parser(lexer)
  interpreter = qint.Interpreter(parser, Variables, args[1])
  interpreter.interpret()

if __name__ == "__main__":
  run(sys.argv)