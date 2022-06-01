# QoLang Standart Library - qo.py
from qclasses import PythonFunc, VarVal
import sys

qolang_export = {
  "args": "args",
  "func_exportAll": "exportAll",
}

args = sys.argv[1:]

def func_exportAll(Variables, args:list):
  """
  Export all variables.
  """
  export = []
  for variable in Variables.vars:
    if not isinstance(variable, PythonFunc):
      export += [variable.name]
  
  Variables.setVar(VarVal("__export__", export))
  return (Variables, None)
