"""
The stack module implements stacks for variables.
"""

from qclasses import VarVal, Tokens, PythonFunc, Token
import sys
import os
qolang_export = {
    "pushstack": "push",
    "popstack": "pop",
    "getstack": "get",
}

stack = {}


def pushstack(Variables, args):
    """
    stack.push(variable)

    Push a variable into its stack.
    """
    if not args[0] in stack:
        stack[args[0]] = []
    stack[args[0]].append(Variables.getVar(args[0]))
    return (Variables, None)


def popstack(Variables, args):
    """
    stack.pop(variable)

    Pop a variable from its stack.
    """
    if not args[0] in stack:
        Variables.setVar(VarVal(args[0], None))
    else:
        Variables.setVar(stack[args[0]].pop())
        # Remove the list if it's empty
        if stack[args[0]] == []:
            del stack[args[0]]
    return (Variables, None)


def getstack(Variables, args):
    """
    stack.get(variable)

    Get the stack of a variable.
    """
    if not args[0] in stack:
        out = []
    else:
        out = [value.value for value in stack[args[0]]]
    return (Variables, out)
