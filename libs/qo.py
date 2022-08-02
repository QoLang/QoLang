# QoLang Standart Library - qo.py
from qclasses import PythonFunc, VarVal
import sys
import os
import qo

qolang_export = {
    "var_args": "args",
    "func_exportAll": "exportAll",
    "func_env": "env",
    "func_version": "version",
}

var_args = sys.argv[1:]


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


def func_version(Variables, args: list):
    """
    QoLang version.
    """
    return (Variables, qo.VERSION)
