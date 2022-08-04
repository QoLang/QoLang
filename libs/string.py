"""
The string module provides functions for working with strings.
"""

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
    string.getAfter(string, seperator)

    Get the content after a seperator in a string.
    """
    return (Variables, args[1].join(args[0].split(args[1])[1:]))


def func_deleteAfter(Variables, args: list):
    """
    string.deleteAfter(string, seperator)

    Delete the content after a seperator in a string.
    """
    return (Variables, args[0].split(args[1])[0])


def func_split(Variables, args: list):
    """
    string.split(string, seperator)

    Split a string with specified seperator.
    """
    return (Variables, args[0].split(args[1]))


def func_replace(Variables, args: list):
    """
    string.replace(string, old, new)

    Replace something with something else in a string.
    """
    return (Variables, args[0].replace(args[1], args[2]))


def func_format(Variables, args: list):
    """
    string.format(string)

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
    string.join(list, seperator)

    Join a list with a delimeter.
    """
    return (Variables, args[1].join(args[0]))


def func_startsWith(Variables, args: list):
    """
    string.startsWith(string, substring)

    Check if string starts with another string.
    """
    return (Variables, args[0].startswith(args[1]))


def func_endsWith(Variables, args: list):
    """
    string.endsWith(string, substring)

    Check if string ends with another string.
    """
    return (Variables, args[0].endswith(args[1]))
