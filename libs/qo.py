"""
The qo module provides functions for working with the current QoLang environment.
"""

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


class var_args:
    """
    qo.args

    The arguments passed to the script.
    """
    theargs = sys.argv[1:]
    qo_callable = False

    def __getter__(self):
        return self.theargs

    def __setter__(self, value):
        self.theargs = value


def func_exportAll(Variables, args: list):
    """
    qo.exportAll()

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
    qo.env(variable)

    Get an environment variable.
    """
    return (Variables, os.environ.get(args[0], None))


def func_version(Variables, args: list):
    """
    qo.version()

    QoLang version.
    """
    return (Variables, qo.VERSION)
