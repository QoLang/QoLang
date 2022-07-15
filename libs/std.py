# QoLang Standard Library
from qclasses import VarVal, Fstring
import sys
import time
import os
import qlexer
import qint
import qparser
import datetime

qolang_export = {
    "func_print": "print",
    "func_println": "println",
    "func_input": "input",
    "func_toInt": "toInt",
    "func_toBool": "toBool",
    "func_toStr": "toStr",
    "func_toFloat": "toFloat",
    "func_type": "type",
    "func_exit": "exit",
    "func_mod": "mod",
    "func_hasAttr": "hasAttr",
    "func_exists": "exists",
    "func_remove": "remove",
    "func_move": "move",
    "func_sleep": "sleep",
    "func_read": "read",
    "func_readlines": "readlines",
    "func_len": "len",
    "func_chr": "chr",
    "func_ord": "ord",
    "func_getAfter": "getAfter",
    "func_deleteAfter": "deleteAfter",
    "func_split": "split",
    "func_replace": "replace",
    "func_format": "format",
    "func_filelist": "filelist",
    "func_join": "join",
    "func_formatdate": "formatdate",
    "func_readlinef": "readlinef",
    "func_writef": "writef",
    "func_appendf": "appendf",
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


def func_toInt(Variables, args: list):
    """
    Convert any type of variable to Int.
    """
    out = 0
    if type(args[0]) in [int, float]:
        out = int(args[0])
    elif type(args[0]) == str:
        try:
            out = int(args[0], 0)
        except:
            out = 0 if args[0] == "" else 1
    elif type(args[0]) == bool:
        out = 1 if args[0] else 0

    return (Variables, out)


def func_toBool(Variables, args: list):
    """
    Convert any type of variable to Bool.
    """
    out = False
    if type(args[0]) in [int, float]:
        out = args[0] == 1
    elif type(args[0]) == str:
        out = args[0] != ""
    elif type(args[0]) == bool:
        out = out

    return (Variables, out)


def func_toStr(Variables, args: list):
    """
    Convert any type of variable to Str.
    """
    out = str(args[0])
    return (Variables, out)


def func_toFloat(Variables, args: list):
    """
    Convert any type of variable to Float.
    """
    out = 0.0
    if type(args[0]) in [int, float]:
        out = float(args[0])
    elif type(args[0]) == str:
        try:
            out = float(args[0])
        except:
            out = 0.0 if args[0] == "" else 1.0
    elif type(args[0]) == bool:
        out = 1.0 if args[0] else 0.0

    return (Variables, out)


def func_type(Variables, args: list):
    """
    Get type of something.
    """
    types = {
        int: "Int",
        str: "Str",
        bool: "Bool",
        float: "Float"
    }
    out = types[type(args[0])]
    return (Variables, out)


def func_exit(Variables, args: list = [0]):
    """
    Exit with code.
    """
    sys.exit(args[0])


def func_mod(Variables, args: list):
    """
    Math modulus function.
    """
    out = args[0] % args[1]
    return (Variables, out)


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


def func_read(Variables, args: list):
    """
    Read a file.
    """
    output = None
    if os.path.isfile(args[0]):
        with open(args[0]) as f:
            output = f.read()
    return (Variables, output)


def func_readlines(Variables, args: list):
    """
    Read lines from a file.
    """
    output = None
    if os.path.isfile(args[0]):
        with open(args[0]) as f:
            output = f.read().splitlines()
    return (Variables, output)


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


def func_getAfter(Variables, args: list):
    """
    Get the content after a seperator in a string.
    """
    return (Variables, args[1].join(args[0].split(args[1])[1:]))


def func_deleteAfter(Variables, args: list):
    """
    Delete the content after a seperator in a string.
    """
    return (Variables, args[0].split(args[1])[0])


def func_split(Variables, args: list):
    """
    Split a string with specified seperator.
    """
    return (Variables, args[0].split(args[1]))


def func_replace(Variables, args: list):
    """
    Replace something with something else in a string.
    """
    return (Variables, args[0].replace(args[1], args[2]))


def func_format(Variables, args: list):
    """
    Format a string.
    """
    out = ""
    lexer = qlexer.Lexer("\0" + args[0] + "\0")
    token = lexer.fstring('\0')
    parser = qparser.Parser(lexer)
    astnode = Fstring(token)
    interpreter = qint.Interpreter(parser, Variables, "String")
    out = interpreter.visit(astnode)
    return (Variables, out)


def func_filelist(Variables, args: list = ["."]):
    """
    Get file list in a directory.
    """
    return (Variables, os.listdir(args[0]))


def func_join(Variables, args: list):
    """
    Join a list with a delimeter.
    """
    return (Variables, args[1].join(args[0]))


def func_formatdate(Variables, args: list):
    """
    Format unix timestamp.
    """
    return (Variables, datetime.datetime.utcfromtimestamp(args[0]).strftime(args[1]))


def func_readlinef(Variables, args: list):
    """
    Read a line from a file.
    """
    output = None
    if os.path.isfile(args[0]):
        with open(args[0]) as f:
            output = f.readline()
    return (Variables, output)


def func_writef(Variables, args: list):
    """
    Write to a file.
    """
    with open(args[0], "w") as f:
        f.write(args[1])
    return (Variables, None)


def func_appendf(Variables, args: list):
    """
    Append to a file.
    """
    with open(args[0], "a") as f:
        f.write(args[1])
    return (Variables, None)
