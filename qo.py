import qlexer
import qparser
from qclasses import PythonFunc, VarVal, Vars, Token, Tokens
Variables = Vars()
import qint
import sys
import runpy
import os

VERSION = "0.3.1"

def run(args, main=False):
  # Load standard library
  if os.name == "nt":
    toinclude = runpy.run_path("C:\\qolang\\libs\\std.py")
  elif os.name == "posix":
    toinclude = runpy.run_path("/usr/lib/qo/std.py")
  else:
    print("This OS is not supported, yet.")
    sys.exit(1)
  for fn in toinclude["qolang_export"]:
    if callable(toinclude[fn]):
      added = PythonFunc(Token(Tokens.FUNCCALL, fn, 0, 0), fn, toinclude[fn])
    else:
      added = VarVal(fn, toinclude[fn])
    Variables.setVar(added)
  Variables.setVar(VarVal("__main__", main))

  contents = open(args[1]).read()
  lexer = qlexer.Lexer(contents)
  parser = qparser.Parser(lexer)
  interpreter = qint.Interpreter(parser, Variables, args[1])
  interpreter.interpret()

if __name__ == "__main__":
  if len(sys.argv) == 1 or sys.argv[1][0] == '-':
    if len(sys.argv) == 1 or sys.argv[1] in ["--help", "-h"]:
      print(f"""QoLang {VERSION}
usage: qolang [file|argument]

arguments:
  --help,    -h   show this message and exit
  --version, -v   show version and exit""")
    elif sys.argv[1] in ["--version", "-v"]:
      print(VERSION)
    else:
      print(f"Unknown argument '{sys.argv[1]}'")
      sys.exit(1)
    sys.exit(0)
  else:
    run(sys.argv, True)
