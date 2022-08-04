"""
The file module provides functions for working with files.
"""

import os
import io
from qclasses import Define, Token, Tokens

qolang_export = {
    "const_SEEK_SET": "SEEK_SET",
    "const_SEEK_CUR": "SEEK_CUR",
    "const_SEEK_END": "SEEK_END",
    "func_open": "open",
    "func_read": "read",
    "func_readlines": "readlines",
    "func_list": "list",
    "func_readline": "readline",
    "func_write": "write",
    "func_close": "close",
    "func_isfile": "isfile",
    "func_isdir": "isdir",
    "func_readable": "readable",
    "func_writable": "writable",
    "func_seekable": "seekable",
    "func_fd": "fd",
    "func_truncate": "truncate",
    "func_flush": "flush",
    "func_tell": "tell",
    "func_seek": "seek",
}

const_SEEK_SET = Define(Token(Tokens.ID, "SEEK_SET", 0, 0))
const_SEEK_CUR = Define(Token(Tokens.ID, "SEEK_CUR", 0, 0))
const_SEEK_END = Define(Token(Tokens.ID, "SEEK_END", 0, 0))
const_SEEK_SET.__doc__ = const_SEEK_CUR.__doc__ = const_SEEK_END.__doc__ = \
    """
    file.SEEK_*

    <code>file.SEEK_SET</code>: Seek from the beginning of the file.
    <code>file.SEEK_CUR</code>: Seek from the current position.
    <code>file.SEEK_END</code>: Seek from the end of the file.

    Mode variables for file.seek(file, offset, mode).
    """


def func_open(Variables, args: list):
    """
    file.open(path, mode)

    Open a file.
    """
    mode = args[1] if len(args) > 1 else "r"
    return (Variables, open(args[0], mode))


def func_read(Variables, args: list):
    """
    file.read(file)
    
    Read a file.
    """
    output = None
    if isinstance(args[0], io.TextIOWrapper):
        output = args[0].read()
    return (Variables, output)


def func_readlines(Variables, args: list):
    """
    file.readlines(file)

    Read lines from a file.
    """
    output = None
    if isinstance(args[0], io.TextIOWrapper):
        output = args[0].readlines()
    return (Variables, output)


def func_list(Variables, args: list = ["."]):
    """
    file.list(path)

    Get file list in a directory.
    """
    return (Variables, os.listdir(args[0]))


def func_readline(Variables, args: list):
    """
    file.readline(file)

    Read a line from a file.
    """
    output = None
    if isinstance(args[0], io.TextIOWrapper):
        output = args[0].readline()
    return (Variables, output)


def func_write(Variables, args: list):
    """
    file.write(file, data)

    Write to a file.
    """
    if isinstance(args[0], io.TextIOWrapper):
        args[0].write(args[1])
    return (Variables, None)


def func_close(Variables, args: list):
    """
    file.close(file)

    Close a file.
    """
    if isinstance(args[0], io.TextIOWrapper):
        args[0].close()
    return (Variables, None)


def func_isfile(Variables, args: list):
    """
    file.isfile(path)

    Check if a path is a file.
    """
    return (Variables, os.path.isfile(args[0]))


def func_isdir(Variables, args: list):
    """
    file.isdir(path)

    Check if a path is a directory.
    """
    return (Variables, os.path.isdir(args[0]))


def func_readable(Variables, args: list):
    """
    file.readable(file)

    Check if a file is readable.
    """
    output = False
    if isinstance(args[0], io.TextIOWrapper):
        output = args[0].readable()
    return (Variables, output)


def func_writable(Variables, args: list):
    """
    file.writable(file)

    Check if a file is writable.
    """
    output = False
    if isinstance(args[0], io.TextIOWrapper):
        output = args[0].writable()
    return (Variables, output)


def func_seekable(Variables, args: list):
    """
    file.seekable(file)

    Check if a file is seekable.
    """
    output = False
    if isinstance(args[0], io.TextIOWrapper):
        output = args[0].seekable()
    return (Variables, output)


def func_fd(Variables, args: list):
    """
    file.fd(file)

    Get a file's file descriptor.
    """
    output = -1
    if isinstance(args[0], io.TextIOWrapper):
        output = args[0].fileno()
    return (Variables, output)


def func_truncate(Variables, args: list):
    """
    file.truncate(file, size)

    Resize a file.
    """
    if isinstance(args[0], io.TextIOWrapper):
        args[0].truncate(args[1])
    return (Variables, None)


def func_flush(Variables, args: list):
    """
    file.flush(file)

    Flush the write buffers of the file.
    """
    if isinstance(args[0], io.TextIOWrapper):
        args[0].flush()
    return (Variables, None)


def func_tell(Variables, args: list):
    """
    file.tell(file)

    Get the current position of the file.
    """
    output = -1
    if isinstance(args[0], io.TextIOWrapper):
        output = args[0].tell()
    return (Variables, output)


def func_seek(Variables, args: list):
    """
    file.seek(file, offset, mode)

    Seek to a position in a file.
    """
    modemap = {
        const_SEEK_SET.value: os.SEEK_SET,
        const_SEEK_CUR.value: os.SEEK_CUR,
        const_SEEK_END.value: os.SEEK_END,
    }
    mode = args[2] if len(args) > 2 else const_SEEK_SET.value
    mode = modemap[mode]
    if isinstance(args[0], io.TextIOWrapper):
        args[0].seek(args[1], mode)
    return (Variables, None)
