# QoLang Standart Library - qo.py
from qclasses import PythonFunc, VarVal
import sys
import os

qolang_export = {
    "args": "args",
    "func_exportAll": "exportAll",
    "func_env": "env",
}

args = sys.argv[1:]


def func_exportAll(Variables, args: list):
    """
    Export all variables.
    """
    export = []
    for variable in Variables.vars:
        if not isinstance(variable, PythonFunc):
            export += [variable.name]

    Variables.setVar(VarVal("__export__", export))
    return (Variables, None)


def func_env(Variables, args: list):
    """
    Get an environment variable.
    """
    return (Variables, os.environ.get(args[0], None))
