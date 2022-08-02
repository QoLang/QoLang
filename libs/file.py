# QoLang Standard Library - file.py
import os
import io

qolang_export = {
    "func_open": "open",
    "func_read": "read",
    "func_readlines": "readlines",
    "func_list": "list",
    "func_readline": "readline",
    "func_write": "write",
    "func_close": "close",
    "func_isfile": "isfile",
    "func_isdir": "isdir",
}


def func_open(Variables, args: list):
    """
    Open a file.
    """
    mode = args[1] if len(args) > 1 else "r"
    return (Variables, open(args[0], mode))


def func_read(Variables, args: list):
    """
    Read a file.
    """
    output = None
    if isinstance(args[0], io.TextIOWrapper):
        output = args[0].read()
    return (Variables, output)


def func_readlines(Variables, args: list):
    """
    Read lines from a file.
    """
    output = None
    if isinstance(args[0], io.TextIOWrapper):
        output = args[0].readlines()
    return (Variables, output)


def func_list(Variables, args: list = ["."]):
    """
    Get file list in a directory.
    """
    return (Variables, os.listdir(args[0]))


def func_readline(Variables, args: list):
    """
    Read a line from a file.
    """
    output = None
    if isinstance(args[0], io.TextIOWrapper):
        output = args[0].readline()
    return (Variables, output)


def func_write(Variables, args: list):
    """
    Write to a file.
    """
    if isinstance(args[0], io.TextIOWrapper):
        args[0].write(args[1])
    return (Variables, None)


def func_close(Variables, args: list):
    """
    Close a file.
    """
    if isinstance(args[0], io.TextIOWrapper):
        args[0].close()
    return (Variables, None)


def func_isfile(Variables, args: list):
    """
    Check if a path is a file.
    """
    return (Variables, os.path.isfile(args[0]))


def func_isdir(Variables, args: list):
    """
    Check if a path is a directory.
    """
    return (Variables, os.path.isdir(args[0]))
