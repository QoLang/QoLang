# QoLang Standard Library
from qclasses import VarVal
import sys
import time
import os
import datetime

qolang_export = {
    "func_print": "print",
    "func_println": "println",
    "func_input": "input",
    "func_exit": "exit",
    "func_hasAttr": "hasAttr",
    "func_exists": "exists",
    "func_remove": "remove",
    "func_move": "move",
    "func_sleep": "sleep",
    "func_len": "len",
    "func_chr": "chr",
    "func_ord": "ord",
    "func_formatdate": "formatdate",
}


def func_print(Variables, args: list):
    """
    Print something, multiple values are joined with " " as delimiter.
    """
    toprint = []
    for arg in args:
        if isinstance(arg, VarVal):
            toprint += [str(arg.value)]
        else:
            toprint += [str(arg)]

    print(" ".join(toprint), end="", flush=True)
    return (Variables, None)


def func_println(Variables, args: list):
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


def func_input(Variables, args: list):
    """
    Get input with specified prompt.
    """
    return (Variables, input(args[0] if len(args) >= 1 else ""))


def func_exit(Variables, args: list = [0]):
    """
    Exit with code.
    """
    sys.exit(args[0])


def func_hasAttr(Variables, args: list):
    """
    Check if a variable has an attribute.
    """
    out = Variables.hasAttr(args[0], args[1])
    return (Variables, out)


def func_exists(Variables, args: list):
    """
    Check if a variable exists.
    """
    out = Variables.exists(args[0])
    return (Variables, out)


def func_remove(Variables, args: list):
    """
    Remove a variable.
    """
    Variables.remove(args[0])
    return (Variables, None)


def func_move(Variables, args: list):
    """
    Move a variable with attributes.
    """
    Variables.move(args[0], args[1])
    return (Variables, None)


def func_sleep(Variables, args: list):
    """
    Sleep n seconds.
    """
    time.sleep(args[0])
    return (Variables, None)


def func_len(Variables, args: list):
    """
    Get length of something.
    """
    return (Variables, len(args[0]))


def func_chr(Variables, args: list):
    """
    Get character by ASCII value.
    """
    return (Variables, chr(args[0]))


def func_ord(Variables, args: list):
    """
    Get ASCII value of character.
    """
    return (Variables, ord(args[0]))


def func_formatdate(Variables, args: list):
    """
    Format unix timestamp.
    """
    return (Variables, datetime.datetime.utcfromtimestamp(args[0]).strftime(args[1]))
