# QoLang Standart Library
from qclasses import VarVal, Var
import sys

available_functions = [
  "func_print",
  "func_println",
  "func_input",
  "func_toInt",
  "func_toBool",
  "func_toStr",
  "func_type",
  "func_exit",
  "func_mod",
]

def func_print(Variables, args:list):
  """
  Print something, multiple values are joined with " " as delimiter.
  """
  toprint = []
  for arg in args:
    if isinstance(arg, VarVal):
      toprint += [str(arg.value)]
    else:
      toprint += [str(arg)]

  print(" ".join(toprint), end="")
  return (Variables, None)

def func_println(Variables, args:list):
  """
  Print something with newline, multiple values are joined with " " as delimiter.
  """
  toprint = []
  for arg in args:
    if isinstance(arg, VarVal):
      toprint += [str(arg.value)]
    else:
      toprint += [str(arg)]

  print(" ".join(toprint))
  return (Variables, None)

def func_input(Variables, args:list):
  """
  Get input with specified prompt.
  """
  return (Variables, input(args[0] if len(args) >= 1 else ""))

def func_toInt(Variables, args:list):
  """
  Convert any type of variable to Int.
  """
  out = 0
  if type(args[0]) == int:
    out = args[0]
  elif type(args[0]) == str:
    try:
      out = int(args[0])
    except:
      out = 0 if args[0] == "" else 1
  elif type(args[0]) == bool:
    out = 1 if args[0] else 0
  
  return (Variables, out)

def func_toBool(Variables, args:list):
  """
  Convert any type of variable to Bool.
  """
  out = False
  if type(args[0]) == int:
    out = args[0] == 1
  elif type(args[0]) == str:
    out = args[0] != ""
  elif type(args[0]) == bool:
    out = out
  
  return (Variables, out)

def func_toStr(Variables, args:list):
  """
  Convert any type of variable to Str.
  """
  out = str(args[0])
  return (Variables, out)

def func_type(Variables, args:list):
  """
  Get type of something.
  """
  types = {
    int: "Int",
    str: "Str",
    bool: "Bool"
  }
  out = types[type(args[0])]
  return (Variables, out)

def func_exit(Variables, args:list = [0]):
  """
  Exit with code.
  """
  sys.exit(args[0])

def func_mod(Variables, args:list):
  """
  Math modulus function.
  """
  out = args[0] % args[1]
  return (Variables, out)

def func_exportAll(Variables, args:list):
  """
  Export all variables.
  """
  export = []
  for variable in Variables.vars:
    if not isinstance(variable, BuiltinFunc):
      export += [variable.name]
  
  Variables.setVar(VarVal("__export__", export))
  return (Variables, None)