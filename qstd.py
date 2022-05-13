# QoLang Standart Library
from qclasses import VarVal, Var

available_functions = ["func_print", "func_println", "func_input"]

def func_print(Variables, args:list):
  toprint = []
  for arg in args:
    if isinstance(arg, Var):
      toprint += [Variables.getVar(arg.value).value]
    else:
      toprint += [arg.value]

  print(" ".join(toprint), end="")
  return Variables

def func_println(Variables, args:list):
  toprint = []
  for arg in args:
    if isinstance(arg, Var):
      toprint += [Variables.getVar(arg.value).value]
    else:
      toprint += [str(arg)]

  print(" ".join(toprint))
  return Variables

def func_input(Variables, args:list):
  inp = input(args[0])
  var = VarVal(name=args[1], value=inp)
  Variables.setVar(var)
  return Variables