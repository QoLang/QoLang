# sus standard library
from sclasses import VarVal, Var

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
      toprint += [arg.value]

  print(" ".join(toprint))
  return Variables

def func_input(Variables, args:list):
  inp = input(args[0].value)
  var = VarVal(name=args[1].value, value=inp)
  Variables.setVar(var)
  return Variables