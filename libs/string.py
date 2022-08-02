# QoLang Standard Library - string.py
from qclasses import Fstring
import qlexer
import qparser
import qint

qolang_export = {
    "func_getAfter": "getAfter",
    "func_deleteAfter": "deleteAfter",
    "func_split": "split",
    "func_replace": "replace",
    "func_format": "format",
    "func_join": "join",
    "func_startsWith": "startsWith",
    "func_endsWith": "endsWith",
}


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


def func_join(Variables, args: list):
    """
    Join a list with a delimeter.
    """
    return (Variables, args[1].join(args[0]))


def func_startsWith(Variables, args: list):
    """
    Check if string starts with another string.
    """
    return (Variables, args[0].startswith(args[1]))


def func_endsWith(Variables, args: list):
    """
    Check if string ends with another string.
    """
    return (Variables, args[0].endswith(args[1]))
