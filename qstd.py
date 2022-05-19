# QoLang Standart Library
from qclasses import VarVal, Var

available_functions = [
  "func_print",
  "func_println",
  "func_input",
  "func_toInt",
  "func_toBool",
  "func_toStr",
  "func_type",
  "func_exit"
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
  return Variables

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
  return Variables

def func_input(Variables, args:list):
  """
  Get input with specified prompt and assign to specified variable.
  """
  inp = input(args[0])
  var = VarVal(name=args[1], value=inp)
  Variables.setVar(var)
  return Variables

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
  var = VarVal(name=args[1], value=out)
  Variables.setVar(var)
  return Variables

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
  var = VarVal(name=args[1], value=out)
  Variables.setVar(var)
  return Variables

def func_toStr(Variables, args:list):
  """
  Convert any type of variable to Str.
  """
  out = str(args[0])
  var = VarVal(name=args[1], value=out)
  Variables.setVar(var)
  return Variables

def func_type(Variables, args:list):
  """
  Get type of something and assign it to specified variable.
  """
  types = {
    int: "Int",
    str: "Str",
    bool: "Bool"
  }
  inp = types[type(args[0])]
  var = VarVal(name=args[1], value=inp)
  Variables.setVar(var)
  return Variables

def func_exit(Variables, args:list = [0]):
  """
  Exit with code.
  """
  exit(args[0])